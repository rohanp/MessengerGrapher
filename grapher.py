import pickle as pkl
from collections import namedtuple, OrderedDict
from datetime import datetime
from urllib.request import urlopen
import json
import warnings
import pandas as pd
from matplotlib import pyplot as plt
from userinfo import START_DATE, END_DATE

warnings.simplefilter(action="ignore", category=FutureWarning)

Message = namedtuple("Message", ['person', 'sent_by_me', 'timestamp', 'sex'])
messages = pkl.load(open("messages.pkl", 'rb'))
print("Total Messages: ", len(messages), "\n")

msgs_by_day = {} # msgs[name] = [] * n_days, populated with message counts

start_date = datetime.strptime(START_DATE, "%m/%d/%y")
end_date = datetime.strptime(END_DATE, "%m/%d/%y")
delta = (end_date - start_date).days

for msg in messages:
    if msg.person in msgs_by_day.keys():
        message_time = msg.timestamp.replace(tzinfo=None)
        if start_date < message_time < end_date:
                idx = (message_time - start_date).days
                msgs_by_day[msg.person][idx] += 1
    else:
        msgs_by_day[msg.person] = [0] * delta

msgs_by_day = OrderedDict(sorted(msgs_by_day.items(), key=lambda i: -sum(i[1])))
data = pd.DataFrame(msgs_by_day, index=pd.date_range(start_date, periods=delta))

def numTalkedToPlot(data, min_messages=1, rolling_window=1):
    talkedTo = data[ min_messages < data ]
    talkedTo = ~pd.isnull(talkedTo)
    toPlot = talkedTo.iloc[:,:].sum(axis=1)
    return toPlot.rolling(rolling_window).mean()

toPlot = numTalkedToPlot(data)
ax = toPlot.plot(title="Number of People Talked to", figsize=(10,3))
ax.set_ylabel("Number of People")
fig = ax.get_figure()
fig.savefig("graphs/number_messaged_by_day.png", bbox_inches='tight')
plt.clf()

def everyonePlot(data, rolling_window=1):
    sum_data = data.iloc[:,:].sum(axis=1)
    return sum_data.rolling(rolling_window).mean()

toPlot = everyonePlot(data, rolling_window=1)
ax = toPlot.plot(title="Messaging Data")
ax.set_ylabel("Number of Messages")
ax.set_xlabel("Date")
ax.set_ylim((0, toPlot.max()*1.1))
fig = ax.get_figure()
fig.savefig("graphs/aggregate_messaging_by_day.png", bbox_inches='tight')

def cumMsgPlot(data, start, end):
    data = data.copy().cumsum(axis=0)
    data = data.iloc[:, start:end]
    return data

toPlot = cumMsgPlot(data, start=0, end=6)
ax = toPlot.plot(title="Cumulative Messaging Data (Top 6 Most Talked To)", legend=True, figsize=(10,7))
ax.set_ylabel("Cumulative Number of Messages")
ax.set_xlabel("Date")
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
fig = ax.get_figure()
fig.savefig("graphs/cumulative_messaging_by_day.png", bbox_inches='tight')

####################

msgs_sex_by_day = {} # msgs[sex] = array of days

for msg in messages:
    if msg.sex in msgs_sex_by_day.keys():
        message_time = msg.timestamp.replace(tzinfo=None)
        if start_date < message_time < end_date:
                idx = (message_time - start_date).days
                msgs_sex_by_day[msg.sex][idx] += 1
    else:
        msgs_sex_by_day[msg.sex] = [0] * delta

msgs_sex_by_day = OrderedDict( sorted(msgs_sex_by_day.items(), key=lambda i: -sum(i[1])) )
sex_data = pd.DataFrame(msgs_sex_by_day, index=pd.date_range(start_date, periods=delta))

toPlot = cumMsgPlot(sex_data, start=0, end=10)

if toPlot.columns[0] == "female":
    color = ['pink', 'lightblue', 'black']
else:
    color = ['lightblue', 'pink', 'black']

ax = toPlot.plot(title="Cumulative Messaging Data by Sex", legend=True,
                 color=color, figsize=(7,5))

ax.set_ylabel("Cumulative Number Messages")
ax.set_xlabel("Date")
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
fig = ax.get_figure()
fig.savefig("graphs/cumulative_messaging_by_sex.png", bbox_inches='tight')

toPlot = sex_data.rolling(5).mean()

ax = toPlot.plot(title="Messaging Data by Sex", legend=True,
                 color=color, figsize=(10,5))
fig = ax.get_figure()
fig.savefig("graphs/messaging_by_sex.png", bbox_inches='tight')

#########################

messages_in_range = filter(lambda x: start_date < x.timestamp.replace(tzinfo=None) < end_date, messages)

df = pd.DataFrame(list(messages_in_range), columns=Message._fields)
df = df[["person", "sent_by_me"]]
df.columns = ["person", "sent"]

df['received'] = pd.Series(~df["sent"], index=df.index)
df['total'] = df['sent'] | df['received']

grouped = df.groupby('person')
sent_received = grouped.sum().sort_values('total', ascending=False)
toPlot = sent_received[["sent", "received"]].ix[:15, :]

ax = toPlot.plot.bar(title="Total Messages Sent/Received (Top 15 Most Talked To)", stacked=True, color=('b', 'r'), figsize=(10, 5))
ax.set_ylabel("Number of Messages")
ax.set_xlabel("Person")

fig = ax.get_figure()
fig.savefig("graphs/total_sent_received_by_person.png", bbox_inches='tight')

print("\nDone! Graphs saved in 'graphs' folder")
