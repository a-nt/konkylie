from sense_hat import SenseHat
from pygame import mixer
import time

# init sense hat
sense = SenseHat()

white = (255,255,255)
black = (0,0,0)


global shake
global volume
global playAudio

startvalue = 0.5
shake = startvalue

starvolume = 0.0
volume = startvolume

global timer
timer = 10

# init audio
mixer.init()
mixer.music.load('stream.mp3')
mixer.music.play(loops=-1, start=0.0)

playAudio = False

# do shit

while True:


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
		timer = 30

	else:
		sense.clear()


	def timeOut(n):
		while n > 0:
			print n
			n = n - 1
			if n == 0:
			print('Timed Out')
			playAudio = False

	timeOut(timer)


	# FADE FUNCTION
	def fadeAudio():
		audioVolume = mixer.music.get_volume()
		global volume

		if playAudio:
			if audioVolume < 0.9:
				volume += 0.01
				print volume
		elif not playAudio:
			if audioVolume > 0.0:
				volume -= 0.01
				print volume

		# make sure volume stays in range
		if volume > 1.0:
			volume = 1.0:
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
				shake = startvalue
				print shake
				print mixer.music.get_volume()
				playAudio = not playAudio
				print playAudio

			if event.direction == 'up':
				shake += 0.01
				print shake
				volume += 0.1
				print volume
			elif event.direction == 'down':
				shake -= 0.01
				print shake
				volume -= 0.1
				print volume

	sense.stick.direction_any = change
	mixer.music.set_volume(volume)
