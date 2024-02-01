import datetime
import uuid

from peewee import CharField, DateTimeField, UUIDField

from infra.database.postgres import BaseModel


class UserBot(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    password = CharField()
    token = CharField()
    chat_id = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)


