from dataclasses import dataclass

from faker import Faker


@dataclass
class User:
    name: str = None
    surname: str = None
    middle_name: str = None
    username: str = None
    email: str = None
    password: str = None
    confirm: str = None


def create_user(name=None, surname=None, middle_name=None, username=None, password=None, email=None):
    fake = Faker()

    name = fake.lexify(text='??????') if name is None else name
    surname = fake.lexify(text='??????') if surname is None else surname
    middle_name = fake.lexify(text='??????') if middle_name is None else middle_name
    username = fake.lexify(text='??????') if username is None else username

    password = fake.password() if password is None else password
    email = fake.email() if email is None else email

    return User(
        name=name,
        surname=surname,
        middle_name=middle_name,
        username=username,
        email=email,
        password=password,
        confirm=password
    )


def bad_field(length=3):
    return Faker().lexify(text='?' * length)
