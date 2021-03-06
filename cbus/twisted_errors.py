#!/usr/bin/env python
# twisted_errors.py - Works around differences in error handling in different versions of Twisted.
# Copyright 2012 Michael Farrell <micolous+git@gmail.com>
# 
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

import twisted.internet.error


__all__ = ['ReactorAlreadyInstalledError']

try:
	ReactorAlreadyInstalledError = twisted.internet.error.ReactorAlreadyInstalledError
except AttributeError:
	# old (10?) versions of twisted raise AssertionError instead of ReactorAlreadyInstalledError
	# Though autobahn doesn't work with Twisted 10.  So will only assist with some issues...
	# Debian 6 has Twisted 10.  May be other issues.  Note requirements file states Twisted 12 minimum.
	ReactorAlreadyInstalledError = AssertionError

