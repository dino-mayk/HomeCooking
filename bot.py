import requests
import json


def send_telegram(text: str, icon: str):
    token = "5386269245:AAGDVEgztCLzjZpjpwVAFm-D1G-1z54_2cc"
    url = "https://api.telegram.org/bot"
    channel_id = "-1001514814642"
    url += token
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