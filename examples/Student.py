from peewee import *


class Student(Model):
    id = PrimaryKeyField()
    name = CITextField()
    age = IntegerField()
    grade = IntegerField()
