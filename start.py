from sense_hat import SenseHat
from pygame import mixer
import time
import vlc

# init sense hat
sense = SenseHat()

white = (255,255,255)
black = (0,0,0)


global shake
global volume
global playAudio

startValue = 0.5
shake = startValue

startVolume = 0.0
volume = startVolume


# init audio
mixer.init()
mixer.music.load('/home/pi/Brutal/konkylie/stream.mp3')
mixer.music.play(loops=-1, start=0.0)

playAudio = False


### LOOPING SHIT

while True:

	# DETECT MOVEMENT
	acceleration = sense.get_accelerometer_raw()
	x = acceleration['x']
	y = acceleration['y']
	z = acceleration['z']

	x = abs(x)
	y = abs(y)
	z = abs(y)

	if x > shake or y > shake or z > shake:
		sense.show_letter("X", white)
		playAudio = True

	else:
		sense.clear()
		playAudio = False



	# FADE AUDIO
	def fadeAudio():
		audioVolume = mixer.music.get_volume()
		global volume

		if playAudio:
			if audioVolume < 0.9:
				volume += 0.01
				#print volume
		elif not playAudio:
			if audioVolume > 0.0:
				volume -= 0.001
				#print volume

		# make sure volume stays in range
		if volume > 1.0:
			volume = 1.0
		if volume < 0.0:
			volume = 0.0

	fadeAudio()




	# JOYSTICK CHANGES
	def change(event):
		global shake
		global volume
		global playAudio
		if event.action == 'pressed':

			if event.direction == 'middle':
				shake = startValue

				playAudio = not playAudio
				print playAudio

			if event.direction == 'up':
				shake += 0.01
				print shake

			elif event.direction == 'down':
				shake -= 0.01
				print shake


	sense.stick.direction_any = change
	mixer.music.set_volume(volume)
