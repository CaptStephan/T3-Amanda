# T3 Manual drive test code
#  This will get incorporated into final code and automated with voice and sensor control
# After taking Intel class, should replace the pygame commands with CV2 since it will be used in other parts of the app
# This Python code is a bit crude and needs to be optimized

import random
import time
import atexit
import os
import boto3
import pygame
import io
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from SimpleGUICS2Pygame.simplegui_lib_keys import Keys
from Raspi_PWM_Servo_Driver import PWM
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

simplegui.Frame._hide_status = True

# create a default drive motor object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

#assign motors to correct pins
LMotor = mh.getMotor(3)
RMotor = mh.getMotor(2)

# Initialise the PWM device using the default address
pwm = PWM(0x6F)

# set frequency, max, and min where servo0=Horiz and servo1=vert
servoMin0 = 155  # Min pulse length out of 4096
servoMid0 = 370
servoMax0 = 585  # Max pulse length out of 4096
servoMin1 = 410  # Min pulse length out of 4096
servoMid1 = 530
servoMax1 = 650  # Max pulse length out of 4096

pwm.setPWMFreq(60) # Set frequency to 60 Hz

# manually set the servo location using pulse length to middle
HorizAngle = 370
pwm.setPWM(0, 0, HorizAngle)
VertAngle = 530
pwm.setPWM(1, 0, VertAngle)

rspeed = 0  #set initial speed to zero
lspeed = 0

# call motor speed for each motor
def motorset(rspeed, lspeed):
    print("Motorset def called.")
    RMotor.setSpeed(rspeed)
    RMotor.run(Raspi_MotorHAT.FORWARD)

    LMotor.setSpeed(lspeed)
    LMotor.run(Raspi_MotorHAT.FORWARD)


#Set up Amazon Web Services Polly interface
class Polly():
    OUTPUT_FORMAT = 'mp3'

    def __init__(self, voiceId):
        self.polly = boto3.client('polly')  # access amazon web service
        self.VOICE_ID = voiceId

    def say(self, textToSpeech):  # get polly response and play directly
        pollyResponse = self.polly.synthesize_speech(Text=textToSpeech, OutputFormat=self.OUTPUT_FORMAT,
                                                     VoiceId=self.VOICE_ID)

        pygame.mixer.init()
        pygame.init()  # this is needed for pygame.event.* and needs to be called after mixer.init() otherwise no sound is played

        if os.name != 'nt':
            pygame.display.set_mode((1, 1))  # doesn't work on windows, required on linux

        with io.BytesIO() as f:  # use a memory stream
            f.write(pollyResponse['AudioStream'].read())  # read audiostream from polly
            f.seek(0)
            pygame.mixer.music.load(f)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.event.set_allowed(pygame.USEREVENT)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
            pygame.event.wait()  # play() is asynchronous. This wait forces the speaking to be finished before closing

        while pygame.mixer.music.get_busy() == True:
            pass

#define key press functions
def keydown(key):
    global rspeed, lspeed, HorizAngle, VertAngle
    if key == simplegui.KEY_MAP["up"]:
        rspeed += 10
        lspeed += 10
        print("Up key pressed")
        print("Increase both motor speeds by 10")
        print("Right motor speed = " + str(rspeed))
        print("Left motor speed = " + str(lspeed))
        motorset(rspeed,lspeed)

    elif key == simplegui.KEY_MAP["left"]:
        rspeed += 10
        lspeed -= 10
        print("Left key pressed")
        print("Increase right motor speed and decrease left motor speed by 10")
        print("Right motor speed = " + str(rspeed))
        print("Left motor speed = " + str(lspeed))
        motorset(rspeed,lspeed)

    elif key == simplegui.KEY_MAP["right"]:
        rspeed -= 10
        lspeed += 10
        print("Right key pressed")
        print("Decrease right motor speed and increase left motor speed by 10")
        print("Right motor speed = " + str(rspeed))
        print("Left motor speed = " + str(lspeed))
        motorset(rspeed,lspeed)

    elif key == simplegui.KEY_MAP["down"]:
        rspeed -= 10
        lspeed -= 10
        print("Down key pressed")
        print("Decrease both motor speeds by 10")
        print("Right motor speed = " + str(rspeed))
        print("Left motor speed = " + str(lspeed))
        motorset(rspeed,lspeed)

    elif key == simplegui.KEY_MAP["s"]:
        rspeed = 0
        lspeed = 0
        print("Key S was pressed, set motor speeds to zero (stop)")
        print("Right motor speed = " + str(rspeed))
        print("Left motor speed = " + str(lspeed))
        motorset(rspeed,lspeed)

    elif key == simplegui.KEY_MAP["i"]:
        tts.say("my name is Amanda, system active")

    elif key == simplegui.KEY_MAP["h"]:
        print("Key U was pressed, move camera up")
        if HorizAngle < 565:
            HorizAngle += 20
        elif HorizAngle >= 585:
            HorizAngle = 585
            print("Can't look up higher...")
            tts.say("Can't look up higher...")
        pwm.setPWM(0, 0, HorizAngle)

    elif key == simplegui.KEY_MAP["j"]:
        print("Key N was pressed, move camera up")
        if HorizAngle > 175:
            HorizAngle -= 20
        elif HorizAngle <= 155:
            HorizAngle = 155
            print("Can't look down lower...")
            tts.say("Can't look down lower...")
        pwm.setPWM(0, 0, HorizAngle)

    elif key == simplegui.KEY_MAP["u"]:
        print("Key H was pressed, move camera left")
        if VertAngle > 430:
            VertAngle -= 20
        elif VertAngle <= 410:
            VertAngle = 410
            print("Can't look more left...")
            tts.say("Can't look more left...")
        pwm.setPWM(1, 0, VertAngle)

    elif key == simplegui.KEY_MAP["n"]:
        print("Key J was pressed, move camera right")
        if VertAngle < 630:
            VertAngle += 20
        elif VertAngle >= 650:
            VertAngle = 650
            print("Can't look more right...")
            tts.say("Can't look more right...")
        pwm.setPWM(1, 0, VertAngle)

#initiallize AWS Polly
tts = Polly("Amy")

#set up game frame and start sim
frame = simplegui.create_frame("T3 Control Box", 260, 460)
frame.add_button('Quit', frame.stop)

frame.set_keydown_handler(keydown)

frame.start()


