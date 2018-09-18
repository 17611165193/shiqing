#-*-coding:utf-8-*-
import datetime

d1 = datetime.datetime.strptime('2012-03-02 7:15:20', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2012-03-02 6:10:20', '%Y-%m-%d %H:%M:%S')
delta = d1 - d2
print (delta.days)
print (delta)
