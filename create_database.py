from concurrent.futures import ProcessPoolExecutor
from data.models import User, Chat
import json
import os
import peewee
from data import db


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
            except peewee.InternalError as e:
                transaction.rollback()
                print(e)
                print("ERROR")
            else:
                transaction.commit()
                print("COMMIT")
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
    data = get_data()
    ids = []
    with ProcessPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        ids = executor.map(create_user, data)
    for element in ids:
        if element:
            print("User id:", element)
    create_default_chat()
