"""cronlib

A package for cron job handling functionality in Python. Adds cron parsing
and auditing functions, enabling a developer to quickly view/manage cron jobs. 

    import cronlib
    cron = cronlib.Cronalyzer()
    allCronJobs = cron.parseAllCrontabs()
    for cj in allCronJobs:
        print cj.command
        print cj.schedule.cronify()
    ...

"""

__version__ = '0.1a'
__author__ = 'Devin Cherry <devincherry^at^gmail^dot^com>'


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
        self.minute = minute
        self.hour = hour
        self.day_of_month = dom
        self.month = month
        self.day_of_week = dow

    def toString(self, form='cron'):
        """
        Returns a printable string representation of the CronSchedule.
        Possible forms are 'cron', 'list'.
        """
        if printFormat == 'list':
            tmpStr = "m   => " + self.minute \
                 + "\nh   => " + self.hour \
                 + "\ndom => " + self.day_of_month \
                 + "\nmon => " + self.month \
                 + "\ndow => " + self.day_of_week + "\n"
            return tmpStr
        return _string.join([self.minute, self.hour, self.day_of_month, self.month, self.day_of_week])


class CronJob:
    """
    A CronJob object holding a user, command, and CronSchedule for this CronJob.
    """
    user = '' 
    command = ''
    schedule = None

    def __init__(self, user, command, schedule):
        self.user = user
        self.command = command
        self.schedule = schedule

    def command(self):
        """
        Prints the command which is run for this CronJob.
        """
        pass

    def schedule(self):
        """
        Prints the schedule for this CronJob in human-readable form.
        """
        pass

    def nextRun(self):
        """
        Prints the next scheduled run time for this CronJob in human-readable form.
        """
        pass


class Cronalyzer:
    """
    A crontab manipulation class. This class provides functions for gathering 
    CronJobs from the local system's various crontab files.
    """

    def __init__(self):
        pass

    def parseSystemCrontab(self):
        """
        Parses the main system crontab, returning a list of CronJob objects.
        """
        systemCrontab = "/etc/crontab"
        commentRegex = _re.compile(r'^[\s]{0,}#.*')
        blankLineRegex = _re.compile(r'^[\s]{0,}$')
        cronJobs = []

        try:
            crontab_f = open(systemCrontab, 'r')
        except:
            if MODULE_DEBUG == 1: 
                _sys.stderr.write("\n\tERROR: failed to open file [%s] for read!\n\n" % systemCrontab)
            return []

        crontab = crontab_f.readlines()
        for line in crontab:
            # skip useless lines
            m = commentRegex.match(line)
            if m:
                continue
            m = blankLineRegex.match(line)
            if m:
                continue

            # if line splits into 7+ tokens, grab it
            parts = line.split()                
            if len(parts) > 6:
                sched = CronSchedule(
                    minute = parts.pop(0), 
                    hour = parts.pop(0),
                    dom = parts.pop(0),
                    month = parts.pop(0),
                    dow = parts.pop(0)
                )
                cronJobs.append(
                    CronJob(
                        user = parts.pop(0),
                        command = _string.join(parts).rstrip(),
                        schedule = sched
                    )
                )
            else:
                # TODO: parse things like "SHELL=/bin/sh"
                pass
        return cronJobs


    def parseUserCrontab(self, user=None):
        """
        Parses a user's crontab, returning a list of CronJob objects.
        If no user is specified, returns a list of all users' CronJob objects on the system.

        Keyword arguments:
        user -- The user who's crontab should be parsed and returned. (optional)
        """

        # find the directory where user crons are stored
        if _os.path.isdir('/var/spool/cron/crontabs'):
            cronDir = "/var/spool/cron/crontabs/"
        elif _os.path.isdir('/var/spool/cron'):
            cronDir = "/var/spool/cron/"
        else:
            if MODULE_DEBUG == 1:
                _sys.stderr.write("\n\tERROR: failed to find user crons directory!\n\n")
            return []

        commentRegex = _re.compile(r'^[\s]{0,}#.*')
        blankLineRegex = _re.compile(r'^[\s]{0,}$')
        cronJobs = []

        # get the list of user crontab files, then iterate over and parse each.
        try:
            files = [f for item in _os.listdir(cronDir) if _os.path.isfile(_string.join(cronDir, item))]
        except:
            if MODULE_DEBUG == 1:
                _sys.stderr.write("\n\tERROR: Could not list user crontabs directory!\n\n")
            return []
        if user:
            crontabFile = _string.join(cronDir, user)
            if f in files:
                try:
                    crontab_f = open(crontabFile, 'r')
                except:
                    if MODULE_DEBUG == 1:
                        _sys.stderr.write("\n\tERROR: failed to open crontab [%s] for read!\n\n" % crontabFile)
                    return []
        else:
            for f in files:
                crontabFile = _string.join(cronDir, f)
                try:
                    crontab_f = open(crontabFile, 'r')
                except:
                    if MODULE_DEBUG == 1: 
                        _sys.stderr.write("\n\tERROR: failed to open file [%s] for read!\n\n" % crontabFile)
                    return None
        
                crontab = crontab_f.readlines()
                for line in crontab:
                    # skip useless lines
                    m = commentRegex.match(line)
                    if m:
                        continue
                    m = blankLineRegex.match(line)
                    if m:
                        continue
        
                    # if line splits into 7+ tokens, grab it
                    parts = line.split()                
                    if len(parts) > 6:
                        sched = CronSchedule(
                            minute = parts.pop(0), 
                            hour = parts.pop(0),
                            dom = parts.pop(0),
                            month = parts.pop(0),
                            dow = parts.pop(0)
                        )
                        cronJobs.append(
                            CronJob(
                                user = f,
                                command = _string.join(parts).rstrip(),
                                schedule = sched
                            )
                        )
                    else:
                        # TODO: parse things like "SHELL=/bin/sh"
                        pass
        return cronJobs


    def parseAllCrontabs(self):
        """
        Parses all crontabs on the system, returning a list of CronJob objects.
        """
        sysCrons = self.parseSystemCrontab()
        userCrons = self.parseUserCrontab()
        return sysCrons + userCrons


# Modeline
# vim:ts=4:et:ai:sw=4
