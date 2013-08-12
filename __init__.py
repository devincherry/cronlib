####################################################################################
#    Copyright (C) 2013  Devin Cherry
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# Devin Cherry
# <devincherry@gmail.com>
####################################################################################

"""cronlib

A package for cron job handling functionality in Python. Adds cron parsing
and auditing functions, enabling a developer to quickly view/manage cron jobs. 

    import cronlib
    cron = cronlib.Cronalyzer()
    allCronJobs = cron.parseAllCrontabs()
    for cj in allCronJobs:
        print cj.schedule.toString(), cj.user, cj.command
    ...

"""

__version__ = '0.1a'
__author__ = 'Devin Cherry <devincherry@gmail.com>'


####
import os as _os
import sys as _sys
import re as _re
import string as _string

MODULE_DEBUG = 1

class CronSchedule:
    """
    A CronSchedule object, holding all individual parts of a CronJob's schedule.
    """
    minute = ''
    hour = ''
    day_of_month = ''
    month = ''
    day_of_week = ''

    def __init__(self, minute, hour, dom, month, dow):
        """
        Instantiate a CronSchedule object.

        ARGS:
        - minute: The minute spec string (in crontab(5) format)
        - hour: The hour spec string (in crontab(5) format)
        - dom: The day-of-month spec string (in crontab(5) format)
        - month: The month spec string (in crontab(5) format)
        - dow: The day-of-week spec string (in crontab(5) format)
        """
        self.minute = minute
        self.hour = hour
        self.day_of_month = dom
        self.month = month
        self.day_of_week = dow

    def toString(self, form='cron'):
        """
        Returns a printable string representation of the CronSchedule.

        KWARGS:
        - form: The desired format of the string (optional). Forms include 'cron', 'list'.
        """
        if form == 'cron':
            return _string.join([self.minute, self.hour, self.day_of_month, self.month, self.day_of_week])
        elif form == 'list':
            tmpStr = "m   => " + self.minute \
                 + "\nh   => " + self.hour \
                 + "\ndom => " + self.day_of_month \
                 + "\nmon => " + self.month \
                 + "\ndow => " + self.day_of_week + "\n"
            return tmpStr
        else:
            return "cronlib: invalid format specified!"    

#    def nextRun(self):
#        """
#        Return a string representation of the next scheduled run time. 
#        """
#        pass


class CronJob:
    """
    A CronJob object holding a user, command, and CronSchedule for this CronJob.
    """
    schedule = None
    user = '' 
    command = ''
    source_file = ''

    def __init__(self, user, command, schedule, src_file):
        """
        Instantiate a CronJob object.

        ARGS:
        - user: The user who this CronJob should run as.
        - command: The full command-line for the CronJob.
        - schedule: A CronSchedule object.
        - src_file: The source file the CronJob was parsed from.
        """
        self.user = user
        self.command = command
        self.schedule = schedule
        self.source_file = src_file

    def toString(self, form='system'):
        """
        Returns a string representation of the CronJob.

        KWARGS:
        - form: The desired format of the returned string. Forms include 'user', 'system', 'cronlib'.
        """
        tmp = ''

        if form == 'user':
            tmp = _string.join([self.schedule.toString(), self.user, self.command])
        elif form == 'system':
            tmp = _string.join([self.schedule.toString(), self.command])
        else:
            tmp = "## cronlib extracted from: %s\n" % self.source_file
            tmp = tmp + _string.join([self.schedule.toString(), self.user, self.command])

        return tmp


class Cronalyzer:
    """
    A crontab manipulation class. This class provides functions for gathering 
    CronJobs from the local system's various crontab files.
    """

    def __init__(self):
        pass


    def _parseCrontab(self, cron_f, cronType='user'):
        """
        Internal parser/cleaner function.
        """
        cronJobs = []
        commentRegex = _re.compile(r'^[\s]{0,}#.*')
        blankLineRegex = _re.compile(r'^[\s]{0,}$')

        # read each line, skipping comment/blank lines, and parse each cron job into a list
        crontab = cron_f.readlines()
        for line in crontab:
            # skip useless lines
            m = commentRegex.match(line)
            if m:
                continue
            m = blankLineRegex.match(line)
            if m:
                continue
        
            # if the line splits into enough parts, parse it into a CronJob and add to the list
            parts = line.split()                
            if (cronType == 'system' and len(parts) > 6) or (cronType == 'user' and len(parts) > 5):
                sched = CronSchedule(
                    minute = parts.pop(0), 
                    hour = parts.pop(0),
                    dom = parts.pop(0),
                    month = parts.pop(0),
                    dow = parts.pop(0)
                )

                # get username from filename if user crontab, from 6th field if system crontab
                if cronType == 'user':
                    cronUser = cron_f.name.split('/')[-1]
                elif cronType == 'system':
                    cronUser = parts.pop(0)

                cronJobs.append(
                    CronJob(
                        user = cronUser,
                        command = _string.join(parts).rstrip(),
                        schedule = sched,
                        src_file = cron_f.name
                    )
                )
            else:
                # TODO: parse things like "SHELL=/bin/sh"
                pass

        return cronJobs


    def _getValidCrontabsFromDirs(self, dirlist):
        """
        Internal function to get a list of valid crontab files from a list of directories.
        """
        crontabs = []

        for d in dirlist:
            for f in _os.listdir(d):
                # skip hidden files
                if _re.search("^\..*", f) != None:
                    continue
                filePath = _string.join([d, f], sep='')
                if _os.path.isfile(filePath):
                    crontabs = crontabs + [filePath]

        return crontabs


    def parseSystemCrontabs(self):
        """
        Parses the main system crontabs, returning a list of CronJob objects.
        """
        systemCrontab = "/etc/crontab"
        systemCronDirs = ["/etc/cron.d/"]
        cronjobs = []

        for f in self._getValidCrontabsFromDirs(systemCronDirs):
            crontab_f = open(f, 'r')
            cronjobs = cronjobs + self._parseCrontab(crontab_f, cronType='system')

        return cronjobs


    def parseUserCrontabs(self, user=None):
        """
        Parses a user's crontab, returning a list of CronJob objects.
        If no user is specified, returns a list of all users' CronJob objects on the system.

        KWARGS:
        user -- The user who's crontab should be parsed and returned. (optional)
        """
        cronJobs = []

        # find the directory where user crons are stored
        if _os.path.isdir('/var/spool/cron/crontabs'):
            cronDir = "/var/spool/cron/crontabs/"
        elif _os.path.isdir('/var/spool/cron'):
            cronDir = "/var/spool/cron/"
        else:
            if MODULE_DEBUG == 1:
                _sys.stderr.write("\n\tERROR: failed to find user crons directory!\n\n")
            # FIXME: maybe we should be raising an exception...?
            return []

        # if a user was specified, if user has a crontab, parse & return the CronJobs
        if user:
            crontabFile = _string.join([cronDir, user], sep='')
            if _os.path.isfile(crontabFile):
                crontab_f = open(crontabFile, 'r')
                return self._parseCrontab(crontab_f, cronType='user')
            else:
                return []

        # if no user specified, read all users' crontabs and return complete list of CronJobs
        else:
            files = self._getValidCrontabsFromDirs([cronDir])

            for f in files:
                crontab_f = open(f, 'r')
                cronJobs = cronJobs + self._parseCrontab(crontab_f, cronType='user')

        return cronJobs


    def parseAllCrontabs(self):
        """
        Parses all crontabs on the system, returning a list of CronJob objects.
        """
        sysCrons = self.parseSystemCrontabs()
        userCrons = self.parseUserCrontabs()
        return sysCrons + userCrons


# Modeline
# vim:ts=4:et:ai:sw=4
