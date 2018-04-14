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

startVolume = 50
volume = startVolume


## ------------------------------------------
## INIT STREAM (VLC)
##

global activateStream
global url
global instance
global player
global media

activateStream = False

# url list
if activateStream:
	url = 'http://edge.mixlr.com/channel/elupc'
else:
	url = '/home/pi/Brutal/konkylie/stream.mp3'

#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

#Define VLC player
player=instance.media_player_new()
media=instance.media_new(url)
player.set_media(media)

#Play the media
player.audio_set_volume(0)
player.play()






## ------------------------------------------
## INIT FILE AUDIO TO STAY ALIVE
##

mixer.init()
mixer.music.load('/home/pi/Brutal/konkylie/activate.mp3')
mixer.music.play()

def preventSleep():
	mixer.music.play()
	time.sleep(60)


## ------------------------------------------



playAudio = False # DEFAULT STATE


## LOOPING SHIT

while True:

	preventSleep()


	def switchAudioSource():
		global activateStream
		global url
		global instance
		global player
		global media

		player.stop()

		if activateStream:
			url = 'http://edge.mixlr.com/channel/elupc'
		else:
			url = '/home/pi/Brutal/konkylie/stream.mp3'

		#define VLC instance
		instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

		#Define VLC player
		player=instance.media_player_new()
		media=instance.media_new(url)
		player.set_media(media)

		player.play()


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
		audioVolume = player.audio_get_volume()
		global volume

		if playAudio:
			if audioVolume < 100:
				volume += 1

		elif not playAudio:
			if audioVolume > 0:
				volume -= 0.1


		# make sure volume stays in range
		if volume > 100:
			volume = 100
		if volume < 0:
			volume = 0

	fadeAudio()




	# JOYSTICK CHANGES
	def change(event):
		global shake
		global volume
		global playAudio
		global activateStream
		if event.action == 'pressed':

			if event.direction == 'middle':

				#shake = startValue

				#playAudio = not playAudio
				activateStream = not activateStream
				print activateStream
				switchAudioSource()

				mixer.music.play()

			if event.direction == 'up':
				#shake += 0.01
				print shake

			elif event.direction == 'down':
				#shake -= 0.01
				print shake


	sense.stick.direction_any = change
	#mixer.music.set_volume(volume)
	player.audio_set_volume(int(volume))
	print player.audio_get_volume()
