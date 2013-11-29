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
# <devincherry[at]gmail[dot]com>
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

__version__ = '0.1b'
__author__ = 'Devin Cherry <devincherry@gmail.com>'

MODULE_DEBUG = False

import os, re, sys, string
import vixie


class Cronalyzer:
    """
    A crontab manipulation class. This class provides functions for gathering 
    CronJobs from the local system's various crontab files.
    """

    def __init__(self):
        pass


    def parseCrontab(self, cron_f, cron_type):
        """
        Internal parser/cleaner function.
        """
        cronJobs = []
        envVars = {}

        # all regexes should ignore leading whitespace...
        commentRegex = re.compile(r'^[\s]{0,}#.*')
        blankLineRegex = re.compile(r'^[\s]{0,}$')
        specialTimespecRegex = re.compile(r'^[\s]{0,}@(?P<special>[a-z]+)')

        # VixieCron v2 allows a max length of 999-chars stored in any env variable, 
        # excluding the '\0' terminator. (see: cron.h, MAX_ENVSTR)
        envVarRegex = re.compile(r'^[\s]{0,}(?P<var>SHELL|PATH|MAILTO)=(?P<value>.*)$')

        # read each line, skipping comment/blank lines, and parse each cron job into a list
        crontab = cron_f.readlines()
        for line in crontab:
            sched = None

            #try:
            # skip useless lines
            m = commentRegex.match(line)
            if m: continue
            m = blankLineRegex.match(line)
            if m: continue
            m = envVarRegex.match(line)
            if m:
                envVars[m.group('var')] = m.group('value')
                continue

            parts = line.split()

            # parse 'special' timespec lines 
            m = specialTimespecRegex.search(parts[0])
            if m:
                specialTimeval = m.groups()[0]
                if specialTimeval in ['hourly','daily','weekly','monthly','yearly','annually']:
                    sched = vixie.CronSchedule(special=specialTimeval)
                    if cron_type == vixie.USER_CRONJOB:
                        parts.pop(0)
                        cronUser = cron_f.name.split('/')[-1]
                    elif cron_type == vixie.SYSTEM_CRONJOB:
                        parts.pop(0)
                        cronUser = parts.pop(0)
                else:
                    if MODULE_DEBUG: sys.stderr.write("WARNING: special timespec '%s' not recognized.\n" % specialTimeval)
                    continue

            # else, parse 'normal' timespec entries
            else:        
                if (cron_type == vixie.SYSTEM_CRONJOB and len(parts) > 6) or (cron_type == vixie.USER_CRONJOB and len(parts) > 5):
                    sched = vixie.CronSchedule(
                        minute = parts.pop(0), 
                        hour = parts.pop(0),
                        dom = parts.pop(0),
                        month = parts.pop(0),
                        dow = parts.pop(0)
                    )
                else:
                    if MODULE_DEBUG: sys.stderr.write("WARNING: cron_type '%s' not recognized.\n" % cron_type)
                    continue
    
                # get username from filename if user crontab, from 6th field if system crontab
                if cron_type == vixie.USER_CRONJOB:
                    cronUser = cron_f.name.split('/')[-1]
                elif cron_type == vixie.SYSTEM_CRONJOB:
                    cronUser = parts.pop(0)
    
            # finally, create our new CronJob, and append it to the list
            cj = vixie.CronJob(
                     user = cronUser,
                     command = string.join(parts).rstrip(),
                     schedule = sched,
                     src_file = cron_f.name
                 )
            cj.updateVars(envVars)
            cronJobs.append(cj)
            #except:
            #    if MODULE_DEBUG: sys.stderr.write("WARNING: skipping unparsable cron entry:\n\t[ %s ]\n" % line.split('\n')[0])
            #    continue
            
        return cronJobs


    def _getValidCrontabsFromDirs(self, dirlist):
        """
        Internal function to get a list of valid crontab files from a list of directories.
        """
        crontabs = []

        for d in dirlist:
            for f in os.listdir(d):
                # skip hidden files
                if re.search("^\..*", f) != None:
                    continue
                filePath = string.join([d, f], sep='')
                if os.path.isfile(filePath):
                    crontabs = crontabs + [filePath]

        return crontabs

    def _getUserCronsDir(self):
        # find the directory where user crons are stored
        if os.path.isdir('/var/spool/cron/crontabs'):
            cronDir = "/var/spool/cron/crontabs/"
        elif os.path.isdir('/var/spool/cron'):
            cronDir = "/var/spool/cron/"
        else:
            raise Exception("Could not determine path to per-user crontabs!")

        return cronDir


    def parseSystemCrontabs(self):
        """
        Parses the main system crontabs, returning a list of CronJob objects.
        """
        systemCrontab = "/etc/crontab"
        systemCronDirs = ["/etc/cron.d/"]
        cronjobs = []

        for f in self._getValidCrontabsFromDirs(systemCronDirs):
            if MODULE_DEBUG: sys.stderr.write("INFO: parsing crontab [%s]\n" % f)
            crontab_f = open(f, 'r')
            cronjobs = cronjobs + self.parseCrontab(crontab_f, vixie.SYSTEM_CRONJOB)

        return cronjobs


    def parseUserCrontab(self, user):
        """
        Parses a user's crontab, returning a list of CronJob objects.

        ARGS:
        user -- The user who's crontab should be parsed and returned. (optional)
        """
        userCronDir = self._getUserCronsDir()
        crontabFile = string.join([userCronDir, user], sep='')
        if os.path.isfile(crontabFile):
            if MODULE_DEBUG: sys.stderr.write("INFO: parsing crontab [%s]\n" % crontabFile)
            crontab_f = open(crontabFile, 'r')
            return self.parseCrontab(crontab_f, vixie.USER_CRONJOB)
        else:
            return []


    def parseAllUserCrontabs(self):
        userCronDir = self._getUserCronsDir()
        files = self._getValidCrontabsFromDirs([userCronDir])
        cronJobs = []

        for f in files:
            if MODULE_DEBUG: sys.stderr.write("INFO: parsing crontab [%s]\n" % f)
            crontab_f = open(f, 'r')
            cronJobs = cronJobs + self.parseCrontab(crontab_f, vixie.USER_CRONJOB)

        return cronJobs


    def parseAllCrontabs(self):
        """
        Parses all crontabs on the system, returning a list of CronJob objects.
        """
        sysCrons = self.parseSystemCrontabs()
        userCrons = self.parseAllUserCrontabs()
        return sysCrons + userCrons


# Modeline
# vim:ts=4:et:ai:sw=4
