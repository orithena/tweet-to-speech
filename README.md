# tweet-to-speech

A script to speak your Twitter timeline using an offline text-to-speech engine.

Developed for RaspberryPi using libttspico and ALSA, but runnable on other
architectures, too.

# Prerequisites

You will need python and git. It's presumably already installed.

You need to install libttspico-utils. On Raspbian, that's currently only
available as source (at least, the libttspico-utils package that contains
the needed pico2wave tool).

	sudo apt-get install fakeroot
	sudo apt-get build-dep libttspico-utils
	mkdir pico_build
	cd pico_build/
	apt-get source libttspico-utils
	cd svox-1.0+git20110131/
	dpkg-buildpackage -rfakeroot -us -uc
	cd ..
	sudo dpkg -i libttspico0_1.0+git20110131-2_armhf.deb libttspico-data_1.0+git20110131-2_all.deb libttspico-utils_1.0+git20110131-2_armhf.
deb 

Test:
	pico2wave -w /tmp/pico.wav -l en-GB "Hello World" && aplay /tmp/pico.wav

You need some python modules.

	sudo pip install pyalsaaudio twython guess-language

# Clone Repository

If you have a github account: Better fork the project and clone your own
repo. Then send me pull requests.

If not:

	git clone https://github.com/orithena/tweet-to-speech.git

# Configure

Copy config.clean.py to config.py and edit it according to the comments there.

You will need a Twitter API key and access tokens to configure it correctly.
Register your app and generate the tokens on apps.twitter.com.

# Run

	python tweet-to-speech.py

# Collaborate

This script needs moar features. Send me pull requests :)

Identified improvements:

  * HTML entities must be converted.
  * Some tweets should not be spoken. If it only contains a link, there's no
    use to speak it.
  * Retweets need special attention.  
  * Some characters or character groups need to be converted to speakable text.
    E.g. "<3" needs a speakable equivalent. Don't get me started on Emojis.
  * Links are horrible to listen to.
  * It should be configurable whether you want to listen to your timeline, a
    list, your notifications or a search query.

