from sense_hat import SenseHat
from pygame import mixer

# init sense hat
sense = SenseHat()

white = (255,255,255)
black = (0,0,0)
global shake
global volume
global playAudio
startvalue = 0.1
shake = startvalue
volume = startvalue

# init audio
mixer.init()
mixer.music.load('crowd.mp3')
mixer.music.play()

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
	else:
		sense.clear()



	def fadeAudio():
		audioVolume = mixer.music.get_volume()
		global volume
		while playAudio:
			while audioVolume < 0.9:
				volume += 0.01
		while not playAudio:
			while audioVolume > 0.0:
				volume -= 0.01




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
				#fadeAudio()
				#mixer.music.set_volume(volume)
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
