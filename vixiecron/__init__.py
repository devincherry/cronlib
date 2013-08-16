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
#
# This is a Python rewrite of Paul Vixie's original work on Vixie Cron.
# All credit for original source should be attributed to Paul Vixie, as indicated
# in the following copyright notice. All python-specific bugs should be attributed
# to me (Devin Cherry) ;-)
# 
## (extracted verbatim from Debian 7 package "cron", version 3.0pl1-124.) 
#
# /* Copyright 1988,1990,1993,1994 by Paul Vixie
#  * All rights reserved
#  *
#  * Distribute freely, except: don't remove my name from the source or
#  * documentation (don't take credit for my work), mark your changes (don't
#  * get me blamed for your possible bugs), don't alter or remove this
#  * notice.  May be sold if buildable source is provided to buyer.  No
#  * warrantee of any kind, express or implied, is included with this
#  * software; use at your own risk, responsibility for damages (if any) to
#  * anyone resulting from the use of this software rests entirely with the
#  * user.
#  *
#  * Send bug reports, bug fixes, enhancements, requests, flames, etc., and
#  * I'll try to keep a version up to date.  I can be reached as follows:
#  * Paul Vixie          <paul@vix.com>          uunet!decwrl!vixie!paul
#  */
# 
# /* cron.h - header for vixie's cron
#  *
#  * $Id: cron.h,v 2.10 1994/01/15 20:43:43 vixie Exp $
#  *
#  * vix 14nov88 [rest of log is in RCS]
#  * vix 14jan87 [0 or 7 can be sunday; thanks, mwm@berkeley]
#  * vix 30dec86 [written]
#  */
################################################################################## 

###
### from cron.h
###
FIRST_MINUTE = 0
LAST_MINUTE = 59
MINUTE_COUNT = (LAST_MINUTE - FIRST_MINUTE + 1)

FIRST_HOUR = 0
LAST_HOUR = 23
HOUR_COUNT = (LAST_HOUR - FIRST_HOUR + 1)

FIRST_DOM = 1
LAST_DOM = 31
DOM_COUNT = (LAST_DOM - FIRST_DOM + 1)

FIRST_MONTH = 1
LAST_MONTH = 12
MONTH_COUNT = (LAST_MONTH - FIRST_MONTH + 1)

# note on DOW: 0 and 7 are both Sunday, for compatibility reasons. 
FIRST_DOW = 0
LAST_DOW = 7
DOW_COUNT = (LAST_DOW - FIRST_DOW + 1)

