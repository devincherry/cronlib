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

class CronSchedule:
    """
    A CronSchedule object, holding all individual parts of a CronJob's schedule.
    """
    minute = ''
    hour = ''
    day_of_month = ''
    month = ''
    day_of_week = ''
    special = ''


    def __init__(self, special='', minute='', hour='', dom='', month='', dow=''):
        """
        Instantiate a CronSchedule object.

        KWARGS:
        - special: A 'special' timespec, such as '@hourly'
        - minute: The minute spec string (in crontab(5) format)
        - hour: The hour spec string (in crontab(5) format)
        - dom: The day-of-month spec string (in crontab(5) format)
        - month: The month spec string (in crontab(5) format)
        - dow: The day-of-week spec string (in crontab(5) format)
        """
        self.special = special
        self.minute = minute
        self.hour = hour
        self.day_of_month = dom
        self.month = month
        self.day_of_week = dow


    def toString(self):
        """
        Returns a printable string representation of the CronSchedule.
        """
        if self.special == '':
            return string.join([self.minute, self.hour, self.day_of_month, self.month, self.day_of_week])
        else:
            return string.join(["@", self.special], sep='')

        return tmpStr


#    def nextRun(self):
#        """
#        Returns an ISO-8601 formatted representation of the next scheduled run time. 
#        (i.e. 2013-12-02T12:14:44+00:00)
#        """
#        pass


# Modeline
# vim:ts=4:et:ai:sw=4
