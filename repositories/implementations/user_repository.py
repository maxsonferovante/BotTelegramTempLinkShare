import traceback

import peewee

from infra.database.postgres import PostgresSQLPeeweeConnection
from repositories.user_bot import UserBot


class UserRepository:

    def __init__(self):
        postgresSQL = PostgresSQLPeeweeConnection()
        postgresSQL.createTables([UserBot])

    def create_user(self, first_name, last_name, email, chat_id, token, password):
        try:
            user = UserBot.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                token=token,
                chat_id=chat_id
            )
            user.save()
            return user

        except Exception as e:
            print(e)
            return traceback.format_exc()


    def get_user_by_email(self, email):
        user = UserBot.get(UserBot.email == email)
        return user

    def get_user_by_chat_id(self, chat_id):
        try:
            user = UserBot.get(UserBot.chat_id == chat_id)
            return user
        except Exception as e:
            print(e)
            return None

    def update_user_token(self, user, token):
        user.token = token
        user.save()
        return user

    def update_user_chat_id(self, user, chat_id):
        user.chat_id = chat_id
        user.save()
        return user

    def get_all_users(self):
        users = UserBot.select()
        return users

    def delete_user(self, user):
        user.delete_instance()
        return user
