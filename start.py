from sense_hat import SenseHat
from pygame import mixer

# init sense hat
sense = SenseHat()

white = (255,255,255)
black = (0,0,0)
global shake
startvalue = 0.1
shake = startvalue

# init audio
mixer.init()
mixer.music.load('crowd-cheering.mp3')
mixer.music.play()

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



	def change(event):
		global shake
		if event.action == 'pressed':
			if event.direction == 'middle':
				shake = startvalue
				print shake
				print mixer.music.get_volume()
			if event.direction == 'up':
				shake += 0.01
				print shake
			elif event.direction == 'down':
				shake -= 0.01
				print shake

	sense.stick.direction_any = change
