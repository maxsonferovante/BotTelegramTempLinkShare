from infra.database.postgres import PostgresSQLPeeweeConnection
from repositories.user import User


class UserRepository:

    def __init__(self):
        PostgresSQLPeeweeConnection().createTables([User])

    def create_user(self, first_name, last_name, email, password, token, chat_id):
        user = User.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            token=token,
            chat_id=chat_id
        )
        return user

    def get_user_by_email(self, email):
        user = User.get(User.email == email)
        return user

    def get_user_by_token(self, token):
        user = User.get(User.token == token)
        return user

    def get_user_by_chat_id(self, chat_id):
        user = User.get(User.chat_id == chat_id)
        return user

    def update_user_token(self, user, token):
        user.token = token
        user.save()
        return user

    def update_user_chat_id(self, user, chat_id):
        user.chat_id = chat_id
        user.save()
        return user

    def get_all_users(self):
        users = User.select()
        return users
    def delete_user(self, user):
        user.delete_instance()
        return user