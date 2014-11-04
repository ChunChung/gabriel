import sys
import numpy as np

import config
import voice as vc

class InstRender:
    SIZE = 18	
    def __init__(self, mosaic):
	#TODO: size?
	assert (mosaic.shape[0] == self.SIZE and mosaic.shape[1] == self.SIZE), "mosaic size should be 32x32"
	# mosaic image
	self.mosaic = mosaic
	
    def start(self, region):
	#set current region
	self.region = region
	# make the section variable mutable
	self.section = 0
	#set initial bricks
	self.bricks = np.empty((self.SIZE, self.SIZE))
	self.bricks.fill(None)
	self.bricks[0:2, :] = config.BLUE
	self.bricks[self.SIZE-2:self.SIZE, :] = config.BLUE
	self.bricks[:, 0:2] = config.BLUE
	self.bricks[:, self.SIZE-2:self.SIZE] = config.BLUE
	if region == config.REGIONS[0] : #top_left
	    voice = vc.START_NEW_TOP_LEFT
	#elif region == config.REGIONS[1] : #top_right
	#elif region == config.REGIONS[2] : #bot_left
	#elif region == config.REGIONS[3] : #bot_right
	
	self.addNewBricks()
	
	init_detect = np.empty((self.SIZE,self.SIZE))
	init_detect.fill(1)
	colors, status = self.compare(init_detect)

	return self.genStartNewResult(colors, status, voice)
    
    def addNewBricks(self):
	#TODO: size ?
	# get region offset
	offset_x = 2 + 8 * (self.section % 2)
	offset_y = 2 + 2 * (self.section / 2)
       
	if self.section % 2 == 0: # 8x2 block
	    for i in range(2):
                for j in range(8):
		    self.bricks[offset_y+i, offset_x+j] = self.mosaic[offset_y+i, offset_x+j]	
	else: # 8x2 block
	    for i in range(2):
                for j in range(8):
                    self.bricks[offset_y+i, offset_x+j] = self.mosaic[offset_y+i, offset_x+j]

	#increment section
	self.section += 1
	
	
	

    def update(self, detects):
	#TODO: size ?
	assert (detects.shape[0] == self.SIZE and detects.shape[1] == self.SIZE), "detect bricks size should be 32x32"
	#elif self.region == config.REGIONS[1] : #top_right
	#elif self.region == config.REGIONS[2] : #bot_left
	#elif self.region == config.REGIONS[3] : #bot_right
	# detect only the detectable bricks on current region
	colors, status = self.compare(detects)

	if any(3 in row for row in status): # if there is any error
	    voice = vc.ERROR_BRICKS 	
	elif any(2 in row for row in status): # if there is any imcomplete
	    voice = 'keep going'
	else:
	    # TODO: start new region if no more new bricks
	    self.addNewBricks()
	    colors, status = self.compare(detects) # update status after add new bricks
	    voice = vc.NEW_BRICKS
	return self.genUpdateResult(colors, status, voice)

    # 0: not activate yet 
    # 1: complete (fixed) 
    # 2: incomplete (expect X but BLUE) blink
    # 3: error color (expect X but Y) highlight
    def compare(self, detects):
	assert (self.bricks.shape[0] == self.SIZE and self.bricks.shape[1] == self.SIZE), "length is not 16x16"
	assert (detects.shape[0] == self.SIZE and detects.shape[1] == self.SIZE), "length is not 16x16"
	colors = np.empty((self.SIZE,self.SIZE), dtype=np.int32)
	status = np.empty((self.SIZE,self.SIZE), dtype=np.int32)
	for i in range(self.SIZE):
	    for j in range(self.SIZE):
		if np.isnan(self.bricks[i, j]):
	    	    colors[i, j] = config.BLUE
	       	    status[i, j] = 0
		elif self.bricks[i, j] == detects[i, j]:
	    	    colors[i, j] = self.bricks[i, j]
                    status[i, j] = 1
		elif detects[i, j] == config.BLUE:
	    	    colors[i, j] = self.bricks[i, j]
	    	    status[i, j] = 2
        	else:
            	    colors[i, j] = self.bricks[i, j]
            	    status[i, j] = 3
	return colors, status

    def genStartNewResult(self, colors, status, voice):
	return self.genResult(config.ACTIONS[0], self.region, colors, status, voice)


    def genUpdateResult(self, colors, status, voice):
	return self.genResult(config.ACTIONS[1], self.region, colors, status, voice)


    def genResult(self, action, region, colors, status, voice):
	result = {"action": action, "bricks": {"colors":colors.tolist(), "status":status.tolist(), "region": region}, "voice": voice}
	return result

if __name__ == '__main__':
    m = np.empty((18, 18), dtype=np.int32)
    m.fill(config.BLUE)
    for i in range(2, 16):
        for j in range(2, 16):
	    m[i, j] = j % 5 + 2
    #print m.tolist()
    ir = InstRender(m)
    result = ir.start(config.REGIONS[0])
    print result
    
    d = np.empty((18, 18), dtype=np.int32)
    d.fill(config.BLUE)
    print "--- detect incomplete, all blue ---"  
    #print ir.bricks
    print ir.update(d)
    
    print "--- detect incomplete, finish partial ---"
    for i in range(2, 4):
        for j in range(2, 4):
	    d[i, j] = m[i, j]
    #print ir.bricks
    print ir.update(d)

    print "--- detect error ---"
    d[2, 4] = 3
    d[2, 5] = 3
    d[3, 4] = 3
    d[3, 5] = 3
    print ir.update(d)

    print "--- detect new bricks ---"
    for i in range(2, 10):
        for j in range(2, 10):
            d[i, j] = m[i, j]
    print ir.update(d)
    #print ir.bricks


