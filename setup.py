# -*- coding: utf-8 -*-
#
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

from distutils.core import setup
from setuptools import find_packages

setup(
    name='cronlib',
    version='0.1b',
    author='Devin Cherry',
    author_email='devincherry[at]gmail[dot]com',
    url='http://github.com/youshoulduseunix/cronlib',
    license='GNU LESSER GENERAL PUBLIC LICENSE, version 2.1',
    description='Interface to Unix/Linux Vixie Cron',
    long_description=open('README.txt').read(),
    zip_safe=False,
    packages=find_packages(),
)

