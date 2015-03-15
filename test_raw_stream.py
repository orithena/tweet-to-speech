#!/usr/bin/python

"""
Just start a TwythonStreamer and print out everything. 

Used for getting examples of the data you have to face.

Colored output:
  sudo pip install betterprint
"""

import twython
from twython import TwythonStreamer
import config
try:
  from betterprint import pprint
except ImportError:
  from pprint import pprint

class MyStreamer(TwythonStreamer):
  def on_success(self, data):
    pprint(data)

  def on_error(self, status_code, data):
    print status_code

stream = MyStreamer(
            config.TWITTER_CONSUMER_KEY, 
            config.TWITTER_CONSUMER_SECRET, 
            config.TWITTER_ACCESS_TOKEN, 
            config.TWITTER_TOKEN_SECRET)

stream.user()
