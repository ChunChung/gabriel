import sys
import numpy as np

import config

class InstRender:
	
    def __init__(self, mosaic):
	assert (len(mosaic) != 32 || len(mosaic[0]) != 32), "mosaic size should be 32x32"
	#add blue frames to mosaic image
	self.mosaic = mosaic
	
    def start(self):
	return self.start(config.REGIONS[0])


    def start(region):
	#set current region
	self.region = region
	#set initial bricks
	self.bricks = []
	blue_list_2 = [config.BLUE for i in range(2)]
	blue_list_32 = [config.BLUE for i in range(32)]
	none_list_30 = [None for i in range(30)]
	if region == config.REGIONS[0] : #top_left
	    voice = voice.START_NEW_TOP_LEFT
	    self.bricks.append(blue_list_32)
	    self.bricks.append(blue_list_32)
	    for k in range(30):
		self.bricks.append(blue_list_2 +  none_list_30)
	else if region == config.REGIONS[1] : #top_right
	    self.bricks.append([config.BLUE for i in range(32)])
            self.bricks.append([config.BLUE for i in range(32)])
	    for k in range(30):
                self.bricks.append(none_list_30 + blue_list_2)
	else if region == config.REGIONS[2] : #bot_left
	    for k in range(30):
                self.bricks.append(blue_list_2 +  none_list_30)
	    self.bricks.append([config.BLUE for i in range(32)])
            self.bricks.append([config.BLUE for i in range(32)])
	else if region == config.REGIONS[3] : #bot_right
	    for k in range(30):
                self.bricks.append(none_list_30 + blue_list_2)
	    self.bricks.append([config.BLUE for i in range(32)])
            self.bricks.append([config.BLUE for i in range(32)])
	return self.genStartNewResult(self.region, self.bricks, voice)
    
    def update(self, detects):
	assert (len(detects) != 32 || len(detects[0]) != 32), "detect bricks size should be 32x32"
	# detect only the detectable bricks on current region
	colors = []
	status = []
	if any error : 
	
	else if all correct:
	 
	voice = ''
	return self.genUpdateResult(self.region, voice)


    def genStartNewResult(region, bricks, voice):

	return genResult(config.ACTIONS[0], , , region, voice)


    def genUpdateResult(region, voice):
	
	return genResult(config.ACTIONS[1], , , region, voice)


    def genResult(action, status, colors, region, voice):
	

	return ''
