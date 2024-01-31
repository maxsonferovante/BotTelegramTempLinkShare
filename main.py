from repositories.implementations.userRepository import UserRepository
from random import randint
if __name__ == '__main__':
    userRepository = UserRepository()

    for i in range(3):
        userRepository.create_user("first_name{0}".format(str(randint(1,1000))), "last_name" + str(i), "email" + str(i), "password" + str(i), "token" + str(i), "chat_id" + str(i))

    for u in userRepository.get_all_users():
        print (u.first_name, u.last_name, u.email, u.password, u.token, u.chat_id)
        userRepository.delete_user(u)


