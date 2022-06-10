import requests
import json


def send_telegram(text: str, icon: str):
    with open('security.json', 'r', encoding='utf8') as security:
        security = json.load(security)
        token = security['bot_token']
        channel_id = security['chat_id']
    url = "https://api.telegram.org/bot"
    url += token
    print(icon)
    if icon != '':
        method = url + "/sendPhoto"
        img = open(icon, 'rb')
        r = requests.post(method, data={"chat_id": channel_id, "caption": text},
                          files={'photo': img})
    else:
        method = url + "/sendMessage"
        r = requests.post(method, data={
            "chat_id": channel_id,
            "text": text
        })