from pygame import mixer
import time
from datetime import datetime

mixer.init()

time12 = {0:'12AM', 1:'1AM', 2:'2AM', 3:'3AM', 4:'4AM', 5:'5AM', 6:'6AM', 7:'7AM', 8:'8AM', 9:'9AM', 10:'10AM', 11:'11AM', 12:'12PM', 13:'1PM', 14:'2PM', 15:'3PM', 16:'4PM', 17:'5PM', 18:'6PM', 19:'7PM', 20:'8PM', 21:'9PM', 22:'10PM', 23:'11PM'}

def hourly_voice_reminder():
	"""
	Plays an hourly voice reminder based on the current time.

	This function continuously checks the current time and plays an audio file corresponding to the current hour.
	It uses the pygame library to play the audio files and the datetime module to get the current time.
	The audio files should be named in the format "<hour>.mp3" where <hour> is the hour in 12-hour format followed by "AM" or "PM".

	Returns:
		None
	"""
	while True:
		now = datetime.now()
		currHour = int(now.strftime("%H"))
		currTime = now.strftime("%M:%S")
		fileName = f"/Audio/{time12[currHour]}.mp3"

		if currTime == "00:00":
			mixer.music.load(fileName)
			mixer.music.play()
			print("<HOURLY VOICE REMINDER>")

		print(datetime.now().strftime("%H:%M:%S"))
		time.sleep(1)

hourly_voice_reminder()
