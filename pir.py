import time
import vlc
from gpiozero import MotionSensor

pin = 4

url = "url internet mp3 stream"
pir = MotionSensor(pin)

#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

#Define VLC player
player=instance.media_player_new()

#Define VLC media
media=instance.media_new(url)

#Set player media
player.set_media(media)

while True:
        print("waiting...")
        pir.wait_for_motion()
        player.play()
        time.sleep(600)
        player.stop()
        time.sleep(1)

