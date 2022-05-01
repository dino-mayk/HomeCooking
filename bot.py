import requests


def send_telegram(text: str):
    token = "5386269245:AAGDVEgztCLzjZpjpwVAFm-D1G-1z54_2cc"
    url = "https://api.telegram.org/bot"
    channel_id = "-1001514814642"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")