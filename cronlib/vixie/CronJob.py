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

import string
import CronTypes

class CronJob:
    """
    A CronJob object holding a user, command, and CronSchedule for this CronJob.
    """
    schedule = None
    user = '' 
    command = ''
    source_file = ''
    env_vars = {}

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
        self.env_vars = {'PATH': '/usr/bin:/bin', 'SHELL': '/bin/sh'}

    def toString(self, form=CronTypes.SYSTEM_CRONJOB):
        """
        Returns a string representation of the CronJob.

        KWARGS:
        - form: The desired format of the returned string. Forms include 'user', 'system', 'cronlib'.
        """
        tmp = ''

        # prepend env vars
        for k in self.env_vars.keys():
            tmp = tmp + k + "=" + self.env_vars[k] + "\n"

        if form == CronTypes.SYSTEM_CRONJOB:
            tmp = tmp + string.join([self.schedule.toString(), self.user, self.command])
        elif form == CronTypes.USER_CRONJOB:
            tmp = tmp + string.join([self.schedule.toString(), self.command])
        else:
            tmp = "## cronlib extracted from: %s\n" % self.source_file + tmp
            tmp = tmp + string.join([self.schedule.toString(), self.user, self.command])

        return tmp

    def updateVars(self, varsDict):
        for k in varsDict.keys():
            self.env_vars[k] = varsDict[k]


# Modeline
# vim:ts=4:et:ai:sw=4
