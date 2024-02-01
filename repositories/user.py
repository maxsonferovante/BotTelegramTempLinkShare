import datetime

from peewee import CharField, DateTimeField

from infra.database.postgres import BaseModel


class User(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    password = CharField()
    token = CharField()
    chat_id = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)


