from playhouse.migrate import *


def run(db):
    migrator = PostgresqlMigrator(db)
    migrate(
        migrator.add_column("student", "age", IntegerField())
    )
