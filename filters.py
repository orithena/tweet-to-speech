# Do not alter the following two lines. They are Definitions. With a capital D.
Allow = True
Deny = False

# Do not speak any tweets that contain any of the following keys:
FILTER_BY_KEY_PRESENT = [
  'retweeted_status',  			# Do not speak RTs
]

# Each rule has the format ('key', 'pattern', Action)
# If tweet['key'] equals pattern, Allow or Deny speaking that tweet,
# then stop evaluating this ruleset.
# If a 'default' key is encountered, the Action there is used immediately.
# The rules are evaluated in the order written here, starting with the first.
FILTER_BY_KEY_VALUE = [
  ('lang', 'en', Allow),		# English is ok
  ('lang', 'de', Allow),		# Yes, I know german
  ('lang', 'jp', Deny),			# I cannot speak japanese.
  ('default', Allow)
]

# Same as above, but here the key values are in a dict. And we have regex patterns.
FILTER_BY_REGEX_MATCH = {
  'text': [
    ('^http[^ ]+$', Deny),		# Don't speak link-only tweets
  ],
  'default': Allow
}

# Simple replacements
REPLACE_TEXT_SIMPLE = {
  u'<3': u'KleinerDrei',		# <3
}

REPLACE_TEXT_REGEX = {
  # not implemented yet
}
