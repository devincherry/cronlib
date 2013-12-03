#!/usr/bin/env python
import os, sys
from cronlib import Cronalyzer, CronTypes, __version__

print "cronlib version %s" % __version__
cron = Cronalyzer()

users = ['mike','devin','yuki']
print "\nParsing individual USER crontabs:"
for u in users:
    for cj in cron.parseUserCrontab(u):
        print cj.toString(print_format=CronTypes.SYSTEM_CRON)

print "\nParsing ALL USER crontabs:"
for cj in cron.parseAllUserCrontabs():
    print cj.toString(print_format=CronTypes.SYSTEM_CRON)

print "\nParsing SYSTEM crontabs:"
for cj in cron.parseSystemCrontabs():
    print cj.toString(print_format=CronTypes.CRONLIB)

print "\nParsing ALL crontabs:"
for cj in cron.parseAllCrontabs():
    print cj.toString(print_format=CronTypes.CRONLIB)


