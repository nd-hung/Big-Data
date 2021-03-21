#!/bin/sh

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.2.jar \
 -file max_temperature_map.py -mapper max_temperature_map.py \
 -file max_temperature_reduce.py -reducer max_temperature_reduce.py \
 -input /user/hdoop/data/lab3/ncdc \
 -output /user/hdoop/data/lab3/output 
