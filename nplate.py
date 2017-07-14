import json
import requests
import time
import urllib

import config
from dbnplate import DBHelper

db = DBHelper()

TOKEN = config.token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
SECRET_ADD_KEY = config.addkey
SECRET_DEL_KEY = config.delkey

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            text = text.upper()
            chat = update["message"]["chat"]["id"]
            items = db.get_items()
            answer = ""
            footer = "\nA HelpSA initiative.\nhttp://www.helpsa.org.za"
            if text == "/START":
                answer = "Welcome to Regbot by HelpSA. Please type the vehicle registration number to check. Please note all no space between letters or numbers. e.g. AA00ZZGP"
            elif text.startswith("/"):
                answer = "Command not found." + footer
            elif text.startswith(SECRET_ADD_KEY):
                numb = text[6:]
                answer = "Number added." + footer
                db.add_item(numb)
            elif text.startswith(SECRET_DEL_KEY):
                numb = text[6:]
                if numb in items:
                    db.delete_item(numb)
                    answer = "Number deleted." + footer
                else:
                    answer = "Number not found." + footer
            elif text in items:
                answer = "Vehicle in lookout database." + footer
            else:
                answer = "Vehicle not in lookout database." + footer
            send_message(answer, chat)
        except KeyError:
            pass

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
