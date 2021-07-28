import os
import json

if not os.path.exists("settings.json"):
    temp_data = {
        "shoppy_api_key": "api key here",
        "discord_bot_token": "token here",
        "bot_customization": {
            "prefix": ".",
            "footer": "N1 Shoppy-bot",
            "footer_icon": "https://i.imgur.com/m4V5V94.png",
            "thumbnail_image": "https://avatars.githubusercontent.com/u/30088307?s=200&v=4",
            "hex_color": "#0000FF"
        }
    }
    with open('settings.json', 'w') as file:
        json.dump(temp_data, file, indent=2)
    print("Please fill in the settings.json file and restart")
    os.system('pause >NUL')


def shoppy_api_key():  # API key can be found at shoppy.gg/user/settings
    with open("settings.json") as file:
        return {"Authorization": json.load(file).get("shoppy_api_key"), "User-Agent": "N1 Shoppy-Bot"}


def discord_token():  # Discord bot token can be made & found at discord.com/developers
    with open("settings.json") as file:
        return json.load(file).get("discord_bot_token")


def base_url():
    return "https://shoppy.gg/api/v1"


# CUSTOMIZATION #
def prefix():
    with open("settings.json") as file:
        return json.load(file)["bot_customization"]["prefix"]


def footer():
    with open("settings.json") as file:
        return json.load(file)["bot_customization"]["footer"]


def footer_icon_url():
    with open("settings.json") as file:
        return json.load(file)["bot_customization"]["footer_icon"]


def thumbnail_image():
    with open("settings.json") as file:
        return json.load(file)["bot_customization"]["thumbnail_image"]


def hex_color():
    with open("settings.json") as file:
        return int(json.load(file)["bot_customization"]["hex_color"].replace("#", "0x"), 0)
