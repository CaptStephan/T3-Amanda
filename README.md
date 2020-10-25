# T3-Amanda
Roaming Safety Robot misc code for Raspberry Pi, a motor hat, camera, Respeaker, and Intel Neural Compute Stick

These are code snipets with original code by CaptStephan and publicly available code from github users (named in the code files). Some code from Intel for use with the Neural Compute Stick. Some code from hardware vendors that came with the hardware used on the demo bot.

# This is a very crude file set and my first github repo.

This is how I set up the demo bot.  Some things may be different for you if you are using different hardware.
Hardware:
- Raspberri Pi Model B+
- Raspberri Pi Motor HAT
- Respeaker 4 mic directional microphone with LED light ring
- RPi camera (not standard one, but one with IR for night images)
- Servo assembly for camera (pan and tilt)
- Two motors for movement
- Round clear plastic robot kit for mounting everything
- AND!!! The Intel Neural Compute Stick (first version)

Start working in your home/pi directory (or directory of your choice, but modify below accordingly).

Set-up sequence for installing I2C motor controller board:
- Enable I2C in raspi-config
- Enable SPI in raspi-config
- sudo apt-get install python-smbus
- sudo apt-get install i2c-tools
- wget https://sourceforge.net/projects/u-geek/files/HATs/Raspi_MotorHAT/Raspi_MotorHAT.tar
- tar xvf Raspi_MotorHAT.tar
- cd Raspi_MotorHAT
- sudo apt-get install python-dev

Next step is the set-up for Respeaker, details from:  http://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/
- sudo apt-get update
- sudo apt-get upgrade
- git clone https://github.com/respeaker/seeed-voicecard.git
- cd seeed-voicecard
- sudo ./install.sh
- reboot
- sudo raspi-config
- Select 7 Advanced Options
- Select A4 Audio
- Select 1 Force 3.5mm ('headphone') jack
- Select Finish
- sudo apt update
- sudo apt install audacity
- audacity
- Open Audacity and select AC108 & 4 channels as input and bcm2835 alsa: - (hw:0:0) as output to test
- record any files needed for training (this is how you get a custom wake word or phrase)
- install APA102 LED requirements
- git clone https://github.com/respeaker/4mics_hat.git
- cd 4mics_hat
- sudo apt install python-virtualenv
- virtualenv --system-site-packages ~/env
- source ~/env/bin/activate
- pip install spidev gpiozero
- Now add the DOA (direction of arrival) requirements:
- sudo apt install libatlas-base-dev
- sudo apt install python-pyaudio
- pip install ./snowboy*.whl
- pip install ./webrtc*.whl
- cd ~/
- git clone https://github.com/voice-engine/voice-engine
- cd voice-engine/
- python setup.py install

That is the basic hardware set-up, more on page links above if needed.

Setting up the Movidius Neural Compute Stick on the Pi is best done following these instructions. Read the whole
thing first and do NOT install the things he says to skip on the NCS and OpenCV. Just follow this carefully:
https://www.pyimagesearch.com/2018/02/12/getting-started-with-the-intel-movidius-neural-compute-stick/

Now you have the set-up complete and the link above gives you some test code to be sure everything is working.
From here you can download the inference model you would like to use and go from there.  My intent would be to
train a new model to recognize unsafe things such as a fire not in the fireplace, a hot iron that is still on
with no person next to it, a child too close to a hot stove, etc. The general idea is generic safety bot.

There are three Python files so far, one for testing movement manually, one for testing the voice command and
LED lights, and one generic trained model from Caffe that recognizes: aeroplane, bicycle, bird, boat, bottle,
bus, car, cat, chair, cow, diningtable, dog, horse, motorbike, person, pottedplant, sheep, sofa, train, tvmonitor.

These would all be combined and more hardware for object detection and avoidance added.  Then the combined code
would include Google Home or Alexa implementation for personal assistant items.
