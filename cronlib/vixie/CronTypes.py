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

"""CronTypes

Provides some static variables for specifying 'types' of crontabs.
For example, a CronTypes.SYSTEM_CRON designates a format that's valid for 
use in crontabs like /etc/cron.d/<crontab_file>. A USER_CRON is for use 
in files like /var/spool/cron/<user> files, etc...

"""

SYSTEM_CRON = 'system'
USER_CRON = 'user'
CRONLIB = 'cronlib'

# Modeline
# vim:ts=4:et:ai:sw=4
