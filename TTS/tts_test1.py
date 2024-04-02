from pygame import mixer
from time import sleep
from datetime import datetime

# Constants
sleeper = 1
lastHour12 = 0

# Variables
mixer.init()

def hourly_voice_reminder():
	"""
	Plays an hourly voice reminder based on the current time.

	This function continuously checks the current time and plays an audio file corresponding to the current hour.
	It uses the pygame library to play the audio files and the datetime module to get the current time.
	The audio files should be named in the format "<hour>.mp3" where <hour> is the hour in 12-hour format followed by "AM" or "PM".

	Returns:
		None
	"""
	global sleeper, lastHour12
	lastHour12 = int(datetime.now().strftime("%I"))

	while True:
		now = datetime.now()
		ampm = now.strftime("%p")
		currSec = int(now.strftime("%S"))
		currMin = int(now.strf("%M"))
		currHour12 = int(now.strftime("%I"))
		
		# File name format: <hour><AM/PM>.mp3
		fileName = f"/Audio/{currHour12}{ampm}.mp3"

		if currSec == 0:
			sleeper = 60

		if currMin == 0:
			sleeper = 600

		if currHour12 != lastHour12:
			sleeper = 1800
			lastHour12 = currHour12
			mixer.music.load(fileName)
			mixer.music.play()
			print("<HOURLY VOICE REMINDER>")

		print(f"{now.strftime('%r')}")
		sleep(sleeper)

hourly_voice_reminder()
