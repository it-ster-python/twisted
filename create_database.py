from concurrent.futures import ProcessPoolExecutor
import json
import os
import peewee
from data import db
from data.models import User, Chat


def get_data():
    with open("user_list.json", "r") as file:
        return json.load(file)


def create_user(data: dict):
    user = User()
    user.login = data.get("login")
    user.password = data.get("password")
    try:
        with db.atomic() as transaction:
            try:
                user.save()
            except peewee.InternalError:
                transaction.rollback()
            else:
                transaction.commit()
    except peewee.IntegrityError:
        print(f"{data.get('login')}: Already exist.")
    return user.id


def create_default_chat():
    try:
        default_chat = Chat.get(name="default")
    except Chat.DoesNotExist:
        default_chat = Chat()
        default_chat.name = "default"
        default_chat.admin = User.get(login="admin")
        default_chat.save()
        users = User.select()
        default_chat.users.add(users)
        default_chat.save()
    else:
        users = User.select()
        for user in users:
            if user not in default_chat.users:
                default_chat.users.add(user)
        default_chat.save()


if __name__ == "__main__":
    users_data = get_data()
    ids = []
    with ProcessPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        ids = executor.map(create_user, users_data)
    for element in ids:
        if element:
            print("User id:", element)
    create_default_chat()
    default_chat = Chat.get(name="default")
    for user in default_chat.users:
        print(user)
