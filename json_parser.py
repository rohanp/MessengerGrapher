"""
This script parses the messages found in the exported data dump (JSON format)
from Facebook into a pickled format that is used by the graphing script.
"""

import pickle as pkl
from collections import namedtuple
from datetime import datetime
import json
from requests import get
import os
from bs4 import BeautifulSoup
from userinfo import ME, API_KEY

if os.path.isfile("name_to_sex.pkl"):
    # Cache this data to avoid making requests to the API if possible
    name_to_sex = pkl.load(open("name_to_sex.pkl", 'rb'))
else:
    name_to_sex = {}

def get_sex(name):
    """
    Guess the gender of the sender based on gender-api.
    """
    if len(name.split(" ")) != 1:
        name = name.split(" ")[0]

    url = "https://gender-api.com/get?key=" + API_KEY + "&name=" + name

    try:
        response = get(url)
        data = response.json()

        return data["gender"]
    except Exception:
        return "unknown"

Message = namedtuple("Message", ['person', 'sent_by_me', 'timestamp', 'sex'])
                            # types: str,      bool,         datetime,     str
messages = []

MESSAGE_DIR = os.path.join("messages", "inbox")

for thread in os.listdir(MESSAGE_DIR): # Iterate through each conversation file
    current_thread = os.path.join(MESSAGE_DIR, thread)
    for convo_file in os.listdir(current_thread):
        try:
            with open(os.path.join(current_thread, convo_file)) as f:
                data = json.load(f)

            participants = data["participants"]
            if len(participants) != 2: # Only want PMs (no group chats)
                continue

            # Extract other person in convo
            # All messages for the thread stored under this person's name
            other_people = filter(lambda n: n != ME,
                            map(lambda p: p["name"],
                            participants))
            thread_name = list(other_people)[0]
            
            # Iterate through each message in the conversation and append its info
            for msg in data["messages"]:
                if "content" in msg:
                    timestamp = datetime.fromtimestamp(msg["timestamp_ms"]/1000)

                    person_sending = msg["sender_name"]
                    sent_by_me = (person_sending == ME)

                    sex = "unknown"
                    if thread_name in name_to_sex:
                        sex = name_to_sex[thread_name]
                    else:
                        sex = get_sex(thread_name)
                        name_to_sex[thread_name] = sex

                    messages.append(Message(thread_name, sent_by_me, timestamp, sex))
        except IsADirectoryError: # Messages folder contains multimedia subdirectories
            continue

pkl.dump(messages, open("messages.pkl", "wb"))
pkl.dump(name_to_sex, open("name_to_sex.pkl", 'wb'))
