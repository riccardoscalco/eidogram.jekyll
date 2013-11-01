#!/usr/bin/python2

from twython import TwythonStreamer

import gzip, pickle, dataset

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        tmp = dict([(i, data[i]) for i in ['text','coordinates','created_at','id'] if i in data])
        if tmp['coordinates']:
            tmp['coordinates'] = str(tmp['coordinates'])
        print tmp
        table.insert(tmp)


    def on_error(self, status_code, data):
        print status_code, data

def goo():
    """
    """
    stream.statuses.filter(track='odio,amo,male,bene,brutto,bello,triste,felice,piacere,dolore,detesto,adoro,piace', language='it') twython 

# add yours keys and tokes here
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


# Requires Authentication as of Twitter API v1.1
stream = MyStreamer(APP_KEY,APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

db = dataset.connect('sqlite:///tweets.db')
table = db['tweet']

goo()

