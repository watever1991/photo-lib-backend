import random
import string


def generate_password(length: int) -> str:
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=length))
    return password
