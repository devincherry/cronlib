#!/usr/bin/env python
import os, sys
import cronlib 

print "cronlib version %s" % cronlib.__version__
cron = cronlib.Cronalyzer()

users = ['mike','devin','yuki']
print "\nParsing individual USER crontabs:"
for u in users:
    for cj in cron.parseUserCrontab(u):
        print cj.toString(form='user')

print "\nParsing ALL USER crontabs:"
for cj in cron.parseAllUserCrontabs():
    print cj.toString(form='user')

print "\nParsing SYSTEM crontabs:"
for cj in cron.parseSystemCrontabs():
    print cj.toString(form='cronlib')

print "\nParsing ALL crontabs:"
for cj in cron.parseAllCrontabs():
    print cj.toString(form='cronlib')


