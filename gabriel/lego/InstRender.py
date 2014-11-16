import sys
import numpy as np

import config
import voice as vc
import task1
import time

class InstRender:
    COOLDOWN = 3
    SIZE = 20
    SEC_SIZE = (SIZE - 2) * 2
    TOTAL_BRICKS = (SIZE-2) * (SIZE-2)
    prev_detects = np.empty((SIZE, SIZE))
    prev_status = np.empty((SIZE, SIZE), dtype=np.int32)	
    def __init__(self, mosaic):
	#TODO: size?
	assert (mosaic.shape[0] == self.SIZE and mosaic.shape[1] == self.SIZE), "mosaic size should be 32x32"
	# mosaic image
	self.mosaic = mosaic
	self.last_time = time.time()
	
    def start(self, region):
	#set current region
	self.region = region
	# make the section variable mutable
	self.section = 0
	self.pin = 0
	#set initial bricks
	self.bricks = np.empty((self.SIZE, self.SIZE))
	self.bricks.fill(config.BLUE)
	#self.bricks[0:2, :] = config.BLUE
	#self.bricks[self.SIZE-2:self.SIZE, :] = config.BLUE
	#self.bricks[:, 0:2] = config.BLUE
	#self.bricks[:, self.SIZE-2:self.SIZE] = config.BLUE
	# activate all BLUE
	#for i in range(self.SIZE):
        #    for j in range(self.SIZE):
 	#        if(self.mosaic[i,j] == config.BLUE):
	#	     self.bricks[i,j] = config.BLUE 
	if region == config.REGIONS[0] : #top_left
	    voice = vc.START_NEW_TOP_LEFT
	#elif region == config.REGIONS[1] : #top_right
	#elif region == config.REGIONS[2] : #bot_left
	#elif region == config.REGIONS[3] : #bot_right
	
	
	init_detect = np.empty((self.SIZE,self.SIZE))
	init_detect.fill(1)

        self.addNewBricks2(init_detect)

	colors, status = self.compare(init_detect)

	return self.genStartNewResult(colors, status, voice)
    
    def addNewBricks1(self):
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
	
    def addNewBricks2(self, detects):
	added = 0
	while added < 8 and self.pin < self.TOTAL_BRICKS:
	    sec = self.pin / self.SEC_SIZE
	    run = self.pin % self.SEC_SIZE
	    x = 2 + (run / 2)
	    y = 17 - (sec * 2) - (run % 2)
	    #print "(", x, y, ")"
	    self.bricks[y, x] = self.mosaic[y, x]
	    if self.bricks[y, x] != config.BLUE:# and self.bricks[y, x] != detects[y, x]: # TODO: skip detect correct
                added += 1
    	    self.pin += 1

    def update(self, detects):
	#TODO: size ?
	assert (detects.shape[0] == self.SIZE and detects.shape[1] == self.SIZE), "detect bricks size should be 32x32"
	# skip if state unchanged
	#if np.array_equal(detects, self.prev_detects):
	#    return ""
	now_time = time.time()
	if (now_time - self.last_time) <= self.COOLDOWN:
	    return ""
	self.last_time = now_time
	# detect only the detectable bricks on current region
	colors, status = self.compare(detects)
	#print "prev:", self.prev_status.tolist()
        #print "status:", status.tolist()
	if np.array_equal(status, self.prev_status):
            return ""
	self.prev_status[:] = status[:]
	if any(3 in row for row in status): # if there is any error
	    voice = vc.ERROR_BRICKS 	
	elif any(2 in row for row in status): # if there is any incomplete
	    if any(4 in row2 for row2 in status):
	        voice = vc.ERROR_BRICKS_ON_BLUE
	    else :
	        voice = vc.MADE_PROGRESS
	else:
	    # TODO: start new region if no more new bricks
	    self.addNewBricks2(detects)
	    colors, status = self.compare(detects) # update status after add new bricks
	    self.prev_status[:] = status[:]
	    if any(4 in row2 for row2 in status):
		voice = vc.NEW_BRICKS_ERROR_ON_BLUE
	    else:
	        voice = vc.NEW_BRICKS
	    if self.pin >= self.TOTAL_BRICKS: 
                return self.genCompleteResult()

	#self.prev_detects[:] = detects[:]
	
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
		colors[i,j] = self.bricks[i,j]
		if self.bricks[i,j] == config.BLUE:
		    if detects[i,j] == config.BLUE:
			status[i,j] = 5 # fix blue 
		    else: 
			status[i,j] = 4 # error if bricks on BLUE region
		else:
		    if detects[i,j] == self.bricks[i,j] or (self.bricks[i,j]!=config.BLUE and self.prev_status[i,j] == 1):
			status[i,j] = 1
		    elif detects[i,j] == config.BLUE:
			status[i,j] = 2 # imcomplete
		    else:
			status[i,j] = 3 #error if bricks color is not match
		#if np.isnan(self.bricks[i, j]):
	    	#    colors[i, j] = config.BLUE
	       	#    status[i, j] = 0
		#elif self.bricks[i, j] == detects[i, j] or (self.bricks[i,j]!=config.BLUE and self.prev_status[i,j]==1):# or self.bricks[i, j] == config.BLUE: # skip checking previous completed bricks, skip BLUE
	    	#    colors[i, j] = self.bricks[i, j]
                #    status[i, j] = 1
		#elif detects[i, j] == config.BLUE:
	    	#    colors[i, j] = self.bricks[i, j]
	    	#    status[i, j] = 2
        	#else:
            	#    colors[i, j] = self.bricks[i, j]
            	#    status[i, j] = 3
	#self.prev_status[:] = status[:]
	return colors, status

    def genStartNewResult(self, colors, status, voice):
	return self.genResult(config.ACTIONS[0], self.region, colors, status, voice)


    def genUpdateResult(self, colors, status, voice):
	return self.genResult(config.ACTIONS[1], self.region, colors, status, voice)

    def genCompleteResult(self):
	return self.genResult(config.ACTIONS[2], "", np.array([]), np.array([]), vc.COMPLETE)

    def genResult(self, action, region, colors, status, voice):
	result = {"action": action, "bricks": {"colors":colors.tolist(), "status":status.tolist(), "region": region}, "voice": voice}
	return result

if __name__ == '__main__':
    m = np.empty((20, 20), dtype=np.int32)
    m.fill(config.BLUE)
    for i in range(2, 18):
        for j in range(2, 18):
	    m[i, j] = j % 6 + 1
    print "mosaic = ", m.tolist()
    print "--- start ---"
    ir = InstRender(m)
    #ir = InstRender(task1.task)
    result = ir.start(config.REGIONS[0])
    print "init bricks = ", ir.bricks.tolist()
    print result
    
    d = np.empty((20, 20), dtype=np.int32)
    d.fill(config.BLUE)
    #print "--- detect incomplete, all blue ---"  
    #print ir.update(d)
    
    print "--- detect incomplete, finish partial ---"
    for i in range(16, 18):
        for j in range(2, 4):
	    d[i, j] = m[i, j]
    #print ir.bricks
    print ir.update(d)
    
    print "--- error on blue ---"
    d[2, 2] = 99 #BLUE region
    d[2, 3] = 99 #BLUE region
    print ir.update(d)

    print "--- detect error ---"
    d[16, 4] = 99
    d[16, 5] = 99
    d[17, 4] = 99
    d[17, 5] = 99
    #d[15, 4] = 99 #BLUE region
    #d[15, 5] = 99 #BLUE region
    print ir.update(d)

    print "--- detect new bricks with error on blue ---"
    for i in range(16, 18):
        for j in range(2, 10):
            d[i, j] = m[i, j]
    print ir.update(d)
    
    print "--- detect new bricks ---"
    for i in range(14, 18):
        for j in range(2, 18):
            d[i, j] = m[i, j]
    d[2,2] = config.BLUE
    d[2,3] = config.BLUE
    print ir.update(d)

    print "--- complete ---"
    for i in range(2, 18):
        for j in range(2, 18):
            d[i, j] = m[i, j]
    print ir.update(d)


