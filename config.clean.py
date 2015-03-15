
# Your "app" tokens and secrets.
# Register your app and generate your keys on apps.twitter.com
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACCESS_TOKEN = ''
TWITTER_TOKEN_SECRET = ''

# Your Mixer settings for audio adjustment during speech. 
# Get a list of possible values for MIXERID by starting a python shell and type the following lines:
#   import alsaaudio
#   alsaaudio.mixers()
MIXERID = u'PCM'

# Mixer volume during speech in percent (0-100)
PLAYVOLUME = 75

# Default language of the text-to-speech engine (if not detectable)
# For supported values, run: pico2wave -l foo -w bar 
# Currently known: 'en-US', 'en-GB', 'de-DE', 'es-ES', 'fr-FR', 'it-IT'
TTSDEFAULTLANG = 'de-DE'
