#!/usr/bin/python
# -*- coding: utf-8 -*-

#
 # -----------------------------------------------------
 # File        fading.py
 # Authors     David <popoklopsi> Ordnung
 # License     GPLv3
 # Web         http://popoklopsi.de
 # -----------------------------------------------------
 # 
 # Copyright (C) 2014-2014 David <popoklopsi> Ordnung
 # 
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # any later version.
 #  
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 # 
 # You should have received a copy of the GNU General Public License
 # along with this program. If not, see <http://www.gnu.org/licenses/>
#





###### CONFIGURE THIS ######

RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

# Number of color changes per step (more is faster, but with less effect)
STEPS = 3

###### END ######




import os
import sys
import termios
import tty
import time
from thread import start_new_thread


r = 255
g = 0
b = 0

factor = 1.0 / 255.0
bright = 1.0
realfactor = factor

abort = False
state = True


def updateColor(color, step):
	color += step
	
	if color > 255:
		return 255
	if color < 0:
		return 0
		
	return color


def setLights(light, brightness):
	if light == 0:
		os.system("echo %i=%f > /dev/pi-blaster" % (RED_PIN, brightness))
	elif light == 1:
		os.system("echo %i=%f > /dev/pi-blaster" % (GREEN_PIN, brightness))
	elif light == 2:
		os.system("echo %i=%f > /dev/pi-blaster" % (BLUE_PIN, brightness))


def getCh():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		
	return ch


def checkKey():
	global realfactor
	global bright
	global state
	global abort
	
	while True:
		c = getCh()
		
		if c == '+':
			bright = bright + 0.05
			realfactor = factor * bright
			
			print "Current brightness: %.2f" % bright
			
		if c == '-' and bright > 0.05:
			bright = bright - 0.05
			realfactor = factor * bright
			
			print "Current brightness: %.2f" % bright
			
		if c == 'p':
			state = False
			print "Pausing..."
			
			time.sleep(0.1)
			
			for x in range(3):
				setLights(x, 0.0)
			
		if c == 'r':
			state = True
			print "Resuming..."
			
		if c == 'c':
			abort = True
			break

start_new_thread(checkKey, ())


print "+ / - = Increase / Decrease brightness"
print "p / r = Pause / Resume"
print "c = Abort Program"


setLights(0, realfactor * float(r))
setLights(1, realfactor * float(g))
setLights(2, realfactor * float(b))


while abort == False:
	if state:
		if r == 255 and b == 0 and g < 255:
			g = updateColor(g, STEPS)
			setLights(1, realfactor * float(g))
		
		elif g == 255 and b == 0 and r > 0:
			r = updateColor(r, -STEPS)
			setLights(0, realfactor * float(r))
		
		elif r == 0 and g == 255 and b < 255:
			b = updateColor(b, STEPS)
			setLights(2, realfactor * float(b))
		
		elif r == 0 and b == 255 and g > 0:
			g = updateColor(g, -STEPS)
			setLights(1, realfactor * float(g))
		
		elif g == 0 and b == 255 and r < 255:
			r = updateColor(r, STEPS)
			setLights(0, realfactor * float(r))
		
		elif r == 255 and g == 0 and b > 0:
			b = updateColor(b, -STEPS)
			setLights(2, realfactor * float(b))
	
print "Aborting..."

for x in range(3):
	setLights(x, 0.0)