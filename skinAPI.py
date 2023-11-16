import requests
from base64 import b64decode
import json
import os

_OUTPUT = 'skins'

_NAME_URL = "https://api.mojang.com/users/profiles/minecraft/{USERNAME}"
# name_url.format(USERNAME=USERNAME)
_UUID_URL = "https://sessionserver.mojang.com/session/minecraft/profile/{UUID}"
# uuid_url.format(UUID=UUID)

if not os.path.exists(_OUTPUT):
    os.makedirs(_OUTPUT)
    print(f"Folder '{_OUTPUT}' created.")
else:
    print(f"Folder '{_OUTPUT}' already exists.")

def __get_response(url, username=''):
    response = requests.get(url)
    if response.status_code == 200:
        if not url.startswith('http://textures.minecraft.net/texture/'):
            data = response.json()
            if url.startswith('https://api.mojang.com/users/profiles/minecraft/'):
                uuid = data['id']
                print(uuid)
                return uuid

            elif url.startswith('https://sessionserver.mojang.com/session/minecraft/profile/'):
                skin_url = json.loads(b64decode(data["properties"][0]['value']).decode('utf-8'))['textures']['SKIN']['url'] 
                print(skin_url)
                return skin_url 

        else:
            with open(f'skins/{username}.png', 'wb') as file:
                file.write(response.content)
                print(f"Image downloaded and saved as {username}.png")

    else:
        if url.startswith('http://textures.minecraft.net/texture/'):
            print("Failed to download the image")
        else:
            print(f"Error: {response.status_code}")
            return 0

def get_skin(username):
    name_url = _NAME_URL.format(USERNAME=username)
    uuid = __get_response(name_url)
    uuid_url = _UUID_URL.format(UUID=uuid)

    if not uuid == 0:
        skin_url = __get_response(uuid_url)
        __get_response(skin_url, username=username)
    else:
        print('user not found')

if __name__ == '__main__':

    username = input('username: ')
    name_url = _NAME_URL.format(USERNAME=username)
    uuid = __get_response(name_url)
    uuid_url = _UUID_URL.format(UUID=uuid)

    if not uuid == 0:
        skin_url = __get_response(uuid_url)
        __get_response(skin_url)
    else:
        print('user not found')

