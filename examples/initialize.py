from Student import Student


def run(db):
    with db.atomic():
        db.create_tables([
            Student
        ])
