import pickle as pkl
from collections import namedtuple
from datetime import datetime, timedelta
import json
from urllib.request import urlopen
import os.path
from bs4 import BeautifulSoup
from userinfo import ME, API_KEY

soup = BeautifulSoup(open("messages.htm", encoding='utf8').read(), 'html.parser')
Message = namedtuple("Message", ['person', 'sent_by_me', 'timestamp', 'sex'])
                         # types: str,      bool,         datetime,     str
messages = []

if os.path.isfile("name_to_sex.pkl"):
    name_to_sex = pkl.load(open("name_to_sex.pkl", 'rb'))
else:
    name_to_sex = {}

def get_sex(name):

    if len(name.split(" ")) != 1:
        name = name.split(" ")[0]

    myKey = API_KEY
    url = "https://gender-api.com/get?key=" + myKey + "&name=" + name

    response = urlopen(url)
    decoded = response.read().decode('utf-8')
    data = json.loads(decoded)

    return data["gender"]

for thread in soup.findAll('div', class_="thread"):

    people = list(map(str.strip, thread.contents[0].split(',')))

    if 2 != len(people): # skip group chats for now
        continue

    person1, person2 = people
    person = person1 if person2 in ME else person2 # who im talking to

    for item in thread.contents[1:]:

        if item.name == "div" and item["class"][0] == "message":

            datestring = item.contents[0].contents[1].contents[0]

            try:
                timestamp = datetime.strptime(datestring, '%A, %B %d, %Y at %I:%M%p')
            except ValueError:
                from dateutil.parser import parse
                timestamp = ' '.join(datestring.split()[-1]) # remove timezone
                timestamp = parse(datestring)

            person_sending = item.contents[0].contents[0].contents[0]
            sent_by_me = person_sending in ME

            if person in name_to_sex.keys():
                sex = name_to_sex[person]
            else:
                try:
                    sex = get_sex(person)
                    name_to_sex[person] = sex
                except Exception:
                    sex = "unknown"

            messages.append(Message(person, sent_by_me, timestamp, sex))

pkl.dump(messages, open("messages.pkl", "wb"))
pkl.dump(name_to_sex, open("name_to_sex.pkl", 'wb'))
