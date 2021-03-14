# -*- encoding: utf-8 -*-
"""
@Author             :  Hao Shen 
@Last Modified by   :  Hao Shen
@Last Modified time :  2021/03/14 13:56:08
@Email              :  shenhao0223sh@gamil.com
@Describe           :  None
"""

# here put the import lib
from peewee import *

db = SqliteDatabase('poetry.db')


class CiAuthor(Model):
    value = IntegerField(primary_key=True)
    name = CharField()
    long_desc = TextField(null=True)
    short_desc = TextField(null=True)

    class Meta:
        database = db  # This model uses the "poetry.db" database.


class Ci(Model):
    value = IntegerField(primary_key=True)
    rhythmic = CharField()
    author = CharField()
    content = TextField(null=True)

    class Meta:
        database = db


def init_table():
    db.connect()
    db.create_tables([Ci, CiAuthor])


if __name__ == '__main__':
    init_table()
