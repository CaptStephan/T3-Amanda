#T3basefile to test basics

from Raspi_PWM_Servo_Driver import PWM
import time
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_4mic_array import DOA
from pixels import pixels

#import the Google Asistant API (pushtotalk.py without the request for enter key to start)
import talkassist

device_id='T3-Amanda'
device_model_id='t3-amanda-my-rpi3-zkf3a2'

# Initialise the PWM device using the default address
pwm = PWM(0x6F)

# set max and min, servo0=Horiz, servo1=vert
servoMin0 = 155  # Min pulse length out of 4096
servoMid0 = 370
servoMax0 = 585  # Max pulse length out of 4096

servoMin1 = 410  # Min pulse length out of 4096
servoMid1 = 530
servoMax1 = 650  # Max pulse length out of 4096

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

# old code to manually input the servo location using pulse length
#HorizAngle = input("What is the horizontal servo setting?")
#pwm.setPWM(0, 0, HorizAngle)
#time.sleep(1)
#VertAngle = input("What is the vertical servo setting?")
#pwm.setPWM(1, 0, VertAngle)
#time.sleep(1)

#Wake on keyword and get the direction, set lights to direction, set camera in general direction
def t3_bot():
    src = Source(rate=16000, channels=4, frames_size=320)
    ch1 = ChannelPicker(channels=4, pick=1)
    kws = KWS()
    doa = DOA(rate=16000)

    src.link(ch1)
    ch1.link(kws)
    src.link(doa)
    pixels.listen()
    pwm.setPWM(0, 0, 370)
    pwm.setPWM(1, 0, 640)

    counter=0

    def on_detected(keyword):
        position = doa.get_direction()
        pixels.wakeup(position)
        print('detected {} at direction {}'.format(keyword, position))
        if position >= 30 and position <= 180:
            pwm.setPWM(0, 0, 175)
            pwm.setPWM(1, 0, 500)
        elif position > 180 and position <= 330:
            pwm.setPWM(0, 0, 560)
            pwm.setPWM(1, 0, 500)
        elif position > 330 or position < 30:
            pwm.setPWM(0, 0, 370)
            pwm.setPWM(1, 0, 6200)
        else:
            pwm.setPWM(0, 0, 370)
            pwm.setPWM(1, 0, 640)

        #talkassist.os.system("espeak 'may i help you'")
        print("How may I help you?")
        print("call google assistant here, delete this line.")

    kws.set_callback(on_detected)

    src.recursive_start()

    while True:
        try:
            time.sleep(1)
            counter+=1
            print("counter is at "+ str(counter))
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    t3_bot()
