import numpy as np
import config

task = np.empty((20, 20), dtype=np.int32)
task[:] = config.BLUE
#task[12:16, 9:11] = config.WHITE
#task[8:12, 9:11] = config.BLACK
#task[6:8, 9:11] = config.WHITE
#task[4:6, 9:11] = config.DARK_GREY

task[16:18, 2:6] = config.BLACK
task[16:18, 6:10] = config.WHITE
task[14:16, 10:14] = config.DARK_GREY
task[12:14, 10:12] = config.WHITE
task[12:14, 12:14] = config.BLACK
task[10:14, 14:16] = config.BLACK

#print task.tolist()
