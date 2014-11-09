import numpy as np
import config

task = np.empty((20, 20), dtype=np.int32)
task[:] = config.BLUE
task[14:18, 9:11] = config.WHITE
task[10:14, 9:11] = config.BLACK
task[8:10, 9:11] = config.BROWN
task[6:8, 9:11] = config.DARK_GREY
task[4:6, 2:6] = config.BLACK
task[4:6, 6:10] = config.WHITE
task[4:6, 10:14] = config.BROWN
task[4:6, 14:18] = config.DARK_GREY

#print task.tolist()
