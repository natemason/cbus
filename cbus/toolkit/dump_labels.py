#!/usr/bin/env python
"""
toolkit/dump_labels.py - Dumps group address and unit metadata from a Toolkit CBZ.
Copyright 2012 Michael Farrell <micolous+git@gmail.com>

This library is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library.  If not, see <http://www.gnu.org/licenses/>.
"""

from cbus.toolkit.cbz import CBZ
from optparse import OptionParser
try:
	import json
except ImportError:
	# python <2.6
	import simplejson as json

def main():
	parser = OptionParser(usage='%prog -i input.cbz -o output.json', version='%prog 1.0')
	parser.add_option('-o', '--output', dest='output', metavar='FILE', help='write output to FILE')
	parser.add_option('-i', '--input', dest='input', metavar='FILE', help='read Toolkit backup from FILE')
	parser.add_option('-p', '--pretty', dest='pretty', metavar='SPACES', help='pretty-prints the output with the specified number of spaces between indent levels')
	options, args = parser.parse_args()

	if options.input == None:
		parser.error('Input filename not given.')

	if options.output == None:
		parser.error('Output filename not given.')

	if options.pretty:
		try:
			pretty = int(options.pretty)
		except ValueError:
			parser.error('Pretty-printing spaces value is not a number.')

		if pretty < 0:
			parser.error('Pretty-printing spaces value must not be negative.')
	else:
		pretty = None

	cbz = CBZ(options.input)
	of = open(options.output, 'wb')

	# read in the labels we need into a structure.
	o = {}

	# iterate through networks
	for network in cbz.root.Project.Network:
		no = {
			'name': unicode(network.TagName),
			'address': int(network.Address),
			'networknumber': int(network.NetworkNumber),
			# don't worry about converting CNI/PCI parameters.
			'applications': {},
			'units': {}
		}
		for application in network.Application:
			ao = {
				'name': unicode(application.TagName),
				'address': int(application.Address),
				'description': unicode(application.Description),
				'groups': {}
			}

			for group in application.Group:
				ao['groups'][int(group.Address)] = unicode(group.TagName)

			no['applications'][int(application.Address)] = ao

		for unit in network.Unit:
			# find the channel configuration
			channels = []
			for parameter in unit.PP:
				if parameter.attrib['Name'] == 'GroupAddress':
					ch = parameter.attrib['Value'].split(' ')
					[channels.append(int('0%s' % (c[2:]) if len(c) == 3 else (c[2:]), 16)) for c in ch]

					#print channels
					#print parameter.attrib['Name'], '=', parameter.attrib['Value']
			no['units'][int(unit.Address)] = {
				'name': unicode(unit.TagName),
				'address': int(unit.Address),
				'unittype': unicode(unit.UnitType),
				'unitname': unicode(unit.UnitName),
				'serial': unicode(unit.SerialNumber),
				'catalog': unicode(unit.CatalogNumber),
				'groups': channels
			}

		o[int(network.Address)] = no

	# dump structure as json.
	json.dump(o, of, indent=pretty)
	of.flush()
	of.close()

if __name__ == '__main__':
	main()

