#from TA re helping with TF OOM errors

'''
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config, ...)
'''

'''
#!/bin/sh
sync; echo 1 > /proc/sys/vm/drop_caches
sync; echo 2 > /proc/sys/vm/drop_caches
sync; echo 3 > /proc/sys/vm/drop_caches
'''

'''
sudo jetson_clocks --store
sudo jetson_clocks
'''