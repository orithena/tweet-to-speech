#!/usr/bin/python

""" 
tweet-to-speech.py

Reads the timeline of a twitter account via audio output (ALSA).

config is just a file named config.py next to this script. Copy
config.clean.py to config.py and enter your own data.
You can generate the keys and register your app on apps.twitter.com

(c) 2015 by Dave Kliczbor <maligree@gmx.de>
Licensed under MIT License. See LICENSE file.
"""

# Non-standard Modules (most likely, you will need to install them):
#   pip install pyalsaaudio twython guess-language
import twython
from twython import TwythonStreamer
import alsaaudio
import guess_language

# Standard modules
from subprocess import call
import thread
import uuid
import os
import re
import HTMLParser

# Local Modules
import config
import filters

debug = True

# We need this lock so spoken tweets will not overlap
# (i.e. we create a message queue using thread locks to 
# allow audio generation and playback to run in parallel)
speechlock = thread.allocate_lock()

def say(text, lang=config.TTSDEFAULTLANG):
  """
  Calls pico2wave for text-to-speech, sets the volume, 
  calls aplay for actually playing the generated sound file
  and then restores the volume.
  """
  fname = "/tmp/picotts-%s.wav" % uuid.uuid4()
  if call(["pico2wave", "-w", fname, "-l", lang, text]) == 0:
    speechlock.acquire()
    mixer = oldvolume = None

    try:
      mixer = alsaaudio.Mixer(config.MIXERID)
      oldvolume = mixer.getvolume()[0]
      mixer.setvolume(config.PLAYVOLUME)
    except Exception as e:
      print("Cannot set volume: %s" % e.message)
    
    call(["aplay", fname])

    try:
      mixer.setvolume(oldvolume)
      mixer.close()
    except: pass

    speechlock.release()
    os.unlink(fname)

def allow_by_key_present(tweet):
  l = list(set(filters.FILTER_BY_KEY_PRESENT).intersection(tweet.keys()))
  if debug and len(l) != 0:
    print("Keys present: %s" % l)
  return len(l) == 0

def allow_by_key_value(tweet):
  for rule in filters.FILTER_BY_KEY_VALUE:
    if rule[0] == 'default':
      return rule[1]
    elif tweet[rule[0]] == rule[1]:
      if debug:
        print("Filter by Key value: %s == %s => %s" % (tweet[rule[0]], rule[1], rule[2]))
      return rule[2]
  return True

def allow_by_regex_match(tweet):
  for key,rulelist in filters.FILTER_BY_REGEX_MATCH.iteritems():
    if key == 'default':
      # interpreting 'default' key specially! then rulelist is assumed to be a bool!
      return rulelist
    for ruleset in rulelist:
      if re.match(ruleset[0], tweet[key]):
        if debug:
          print("Filter by regex match: %s matches on %s => %s" % (ruleset[0], tweet[key], ruleset[1]))
        return ruleset[1]
  return True

def allow_tweet(tweet):
  #try:
    return allow_by_key_present(tweet) and allow_by_key_value(tweet) and allow_by_regex_match(tweet)
  #except Exception as e:
  #  print("Config broken? %s" % e)
  #return True

def replace_text(text):
  h = HTMLParser.HTMLParser()
  text = unicode(h.unescape(text))
  for pattern,replacement in filters.REPLACE_TEXT_SIMPLE.iteritems():
    text = text.replace(pattern, replacement)
  # filters.REPLACE_TEXT_REGEX has to be implemented here
  return text

class MyStreamer(TwythonStreamer):
  def on_success(self, tweet):
    """
    Callback method whenever something comes in from the Twitter Streaming API.
    
    tweet is a multi-level dict, containing all metadata of a tweet (sometimes 
    it's not a tweet, it also might be a deletion or fav notice etc).
    """
    if 'text' in tweet:
      # build the string to say
      text = ("%s: %s" % (tweet['user']['screen_name'], tweet['text']))

      # guess language of the tweet
      guessedlang = guess_language.guessLanguage(tweet['text'])
      lang = config.TTSDEFAULTLANG
      try:
        # translate guessed language into language codes accepted by pico2wave
        lang = {'en': 'en-GB', 'de': 'de-DE', 'es': 'es-ES', 'fr': 'fr-FR'}[guessedlang]
      except KeyError:
        pass

      if allow_tweet(tweet):
        text = replace_text(text)
        print "%s (%s)" % (text, lang)
        # start a new thread for saying something.
        # this avoids some weird behaviour, like lagging behind the timeline
        thread.start_new_thread(say, (text, lang))
      else:
        print "Omitted: %s (%s)" % (text, lang)
        
    else:
      print("unknown notification received:")
      print(tweet)

  def on_error(self, status_code, tweet):
    print(status_code)

# Initialize Twitter Streaming API
stream = MyStreamer(
            config.TWITTER_CONSUMER_KEY, 
            config.TWITTER_CONSUMER_SECRET, 
            config.TWITTER_ACCESS_TOKEN, 
            config.TWITTER_TOKEN_SECRET)
# Go into reading loop. Whenever something comes in, MyStreamer.on_success() will be called.
stream.user()
