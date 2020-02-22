# T3-Amanda
Roaming Safety Robot misc code for Raspberry Pi, a motor hat, camera, Respeaker, and Intel Neural Compute Stick

These are code snipets with original code by CaptStephan and publicly available code from github users (named in the code files). Some code from Intel for use with the Neural Compute Stick. Some code from hardware vendors that came with the hardware used on the demo bot.

This is a very crude file set and my first github repo.

This is a running list of things I have found useful or have used to help get set up:

LED Control:
	https://github.com/Psychokiller1888/snipsLedControl/

Color table:
	https://rgbcolorcode.com

Purple RGB = 0x2e0854
Purple R,G,B = (89,0,179)

Set-up sequence for installing I2C motor controller board and Respeaker:
▪	Enable I2C in raspi-config
▪	Enable SPI in raspi-config
▪	Enable sudo apt-get install python-smbus
▪	sudo apt-get install i2c-tools
▪	wget https://sourceforge.net/projects/u-geek/files/HATs/Raspi_MotorHAT/Raspi_MotorHAT.tar
▪	tar xvzf Raspi_MotorHAT.tar
▪	cd Raspi_MotorHAT
▪	sudo apt-get install python-dev
▪	#next step is the set-up for Respeaker, details from:  http://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/

▪	sudo apt-get update
▪	sudo apt-get upgrade
▪	git clone https://github.com/respeaker/seeed-voicecard.git
▪	cd seeed-voicecard
▪	sudo ./install.sh
▪	reboot
▪	sudo raspi-config
▪	# Select 7 Advanced Options
▪	# Select A4 Audio
▪	# Select 1 Force 3.5mm ('headphone') jack
▪	# Select Finish
▪	sudo apt update
▪	sudo apt install audacity
▪	audacity
▪	#Open Audacity and select AC108 & 4 channels as input and bcm2835 alsa: - (hw:0:0) as output to test
▪	#record any files needed for training
▪	#install APA102 LED requirements
▪	git clone https://github.com/respeaker/4mics_hat.git
▪	cd 4mics_hat
▪	sudo apt install python-virtualenv
▪	virtualenv --system-site-packages ~/env
▪	source ~/env/bin/activate
▪	pip install spidev gpiozero
▪	#add the DOA requirements
▪	sudo apt install libatlas-base-dev
▪	sudo apt install python-pyaudio
▪	pip install ./snowboy*.whl
▪	pip install ./webrtc*.whl
▪	cd ~/
▪	git clone https://github.com/voice-engine/voice-engine
▪	cd voice-engine/
▪	python setup.py install
▪	#that is the basic set-up, more on the page at the link above if needed.

Setting up the Movidius Neural Compute Stick on the Pi:
https://www.pyimagesearch.com/2018/02/12/getting-started-with-the-intel-movidius-neural-compute-stick/

https://www.bouvet.no/bouvet-deler/adding-ai-to-edge-devices-with-the-movidius-neural-compute-stick


Making a backup image:
https://thepihut.com/blogs/raspberry-pi-tutorials/17789160-backing-up-and-restoring-your-raspberry-pis-sd-card
