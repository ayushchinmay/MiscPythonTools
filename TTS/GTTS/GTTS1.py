from gtts import gTTS
import pyttsx3
from pygame import mixer

def main():
	while True:
		mixer.init()
		engine = pyttsx3.init()
		speak = input("Enter something: ")

		engine.say(speak)
		engine.runAndWait()


if __name__ == '__main__':
	main()