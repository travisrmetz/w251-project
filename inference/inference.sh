#!/bin/sh
sync; echo 1 > /proc/sys/vm/drop_caches
sync; echo 2 > /proc/sys/vm/drop_caches
sync; echo 3 > /proc/sys/vm/drop_caches

#maximizes performance - can run from container?
sudo jetson_clocks

python3 inference_v2.py