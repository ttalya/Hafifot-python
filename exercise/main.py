import datetime
import shutil
import uuid
from ast import literal_eval
from functools import reduce
import os

# 1


NUM_DICT = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def return_num(num_name):
    return (NUM_DICT.get(num_name, False))


# 2


def calc_sum(num_list):
    return reduce(lambda x, y: x + y, num_list, 0)


# 3


CHARS_TO_REMOVE = ['a', 'u', 'e', 'o', 'i']


def remove_chars(str):
    return ''.join(c for c in str if c not in CHARS_TO_REMOVE)


# 4


def count_num_appear(lower_num, higher_num):
    # return ''.join(str(i) for i in range(lower_num, higher_num + 1)).replace('0', '8').count('8')
    return sum(str(i).count('0') + str(i).count('8') for i in range(lower_num, higher_num + 1))


# 5


def save_data(doc, objs):
    with open(doc, 'a') as file:
        file.writelines(str(type(o)) + ' : ' + str(o) + '\n' for o in objs)
        file.close()


def load_data(doc):
    with open(doc) as file:
        return [(literal_eval(line.split(" : ")[1][:-1])) for line in file]


# 6


def days_to_bd(birthdate):
    today = datetime.datetime.now()
    return (birthdate.replace(year=today.year + 1) - today).days % 365


# 7


def move_tree(src_path, dest_path, name='*'):
    for file in src_path.rglob('*.' + name):
        relative_path = file.relative_to(src_path)
        dest_file = dest_path / relative_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, dest_file)


# 8


import os
import base64
from azure.identity import InteractiveBrowserCredential
from azure.storage.blob import BlobServiceClient

browser_credential = InteractiveBrowserCredential()

account_url = "https://onboardingpractice.blob.core.windows.net"
container_name = "python"
new_account_url = "https://talya.blob.core.windows.net"
new_container_name = "python-talya"

blob_service_client = BlobServiceClient(account_url=account_url, credential=browser_credential)
new_blob_service_client = BlobServiceClient(account_url=new_account_url, credential=browser_credential)

container_client = blob_service_client.get_container_client(container_name)
new_container_client = new_blob_service_client.get_container_client(new_container_name)

blob_list = container_client.list_blobs()

for blob_file in blob_list:
    local_file_name = blob_file.name
    download_file_path = os.path.join('./', local_file_name)
    with open(download_file_path, mode='wb') as file:
        content = blob_service_client.get_blob_client(container=container_name,
                                                      blob=local_file_name).download_blob().readall()
        decoded_content = base64.b64decode(content).decode('utf-8')
        file.write(decoded_content.encode('utf-8'))

    with open(download_file_path, mode="rb") as data:
        new_blob_client = new_container_client.get_blob_client(blob=local_file_name)
        new_blob_client.upload_blob(data)
