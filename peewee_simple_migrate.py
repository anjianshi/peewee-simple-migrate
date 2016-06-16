__all__ = ["need_migrate", "run"]

from peewee import Model, IntegerField, DateTimeField
import logging
import os
from glob import glob
import re
from datetime import datetime
import importlib
import sys

logger = logging.getLogger("peewee-simple-migrate")


class MigrationError(Exception):
    pass


def generate_model(db):
    class Migration(Model):
        """This model it self can't be migrated, so don't change it's structure unless necessary."""
        version = IntegerField(primary_key=True)
        latest_migrate = DateTimeField(null=False)

        class Meta:
            database = db

    return Migration


def get_versions(migration_dir):
    migrate_files = glob(os.path.join(migration_dir, "ver_[0-9]*.py"))

    # Put the version 0 into version list.
    # It represent the initial version of the data structure, and there's not a ver_xxx.py file for it.
    versions = [0]
    for name in migrate_files:
        match = re.search(r"ver_(\d+)\.py$", name).groups()[0]
        versions.append(int(match))
    versions.sort()

    return versions


def execute_migrate_code(migration_dir, module_name, db):
    sys.path.insert(0, os.path.abspath(migration_dir))

    module = importlib.import_module(module_name)
    module.run(db)

    sys.path = sys.path[1:]


def prepare(db, migration_dir):
    Migration = generate_model(db)
    versions = get_versions(migration_dir)

    need_migration = False
    current_version = None      # None means it needs initialize

    if Migration.table_exists():
        current_version = Migration.select().get().version
        if current_version not in versions:
            raise MigrationError("version '{}' not found in local".format(current_version))
        if current_version != versions[-1]:
            need_migration = True
    else:
        need_migration = True

    return [need_migration, current_version, Migration, versions]


def need_migrate(db, migration_dir):
    """return: bool"""
    return prepare(db, migration_dir)[0]


def run(db, migration_dir, check_only=False):
    [need_migration, current_version, Migration, versions] = prepare(db, migration_dir)

    if not need_migration:
        logger.debug("Already latest version {}, doesn't need migrate.".format(current_version))
        return

    if current_version is None:
        if os.path.exists(os.path.join(migration_dir, "initialize.py")):
            with db.transaction():
                execute_migrate_code(migration_dir, "initialize", db)

                db.create_tables([Migration], safe=True)
                Migration.create(version=versions[-1] if len(versions) > 0 else 0,
                                 latest_migrate=datetime.now())

            logger.info("initialize complete, version {}.".format(versions[-1]))
        else:
            raise MigrationError("initialize.py not found")
    else:
        with db.transaction():
            for version in versions:
                if version > current_version:
                    module_name = "ver_{}".format(version)
                    execute_migrate_code(migration_dir, module_name, db)

            query = Migration.update(version=versions[-1], latest_migrate=datetime.now())
            query.execute()

            logger.info("from version {} to {}, migrate complete.".format(current_version, versions[-1]))
