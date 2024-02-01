import random
import string


def generated_user_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))