from concurrent.futures import ProcessPoolExecutor
from data.models import User
import json
import os
import peewee


def get_data():
    with open("user_list.json", "r") as file:
        return json.load(file)


def create_user(data: dict):
    user = User()
    user.login = data.get("login")
    user.password = data.get("password")
    try:
        user.save()
    except peewee.IntegrityError:
        print(f"{data.get('login')}: Already exist.")
    return user.id


if __name__ == "__main__":
    data = get_data()
    ids = []
    with ProcessPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        ids = executor.map(create_user, data)
    for element in ids:
        if element:
            print("User id:", element)
