#
# CIA open source notification system
# Copyright (C) 2003-2007 Micah Dowty <micah@navi.cx>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import re, posixpath, socket
from xml.dom import minidom
from xml.sax import saxutils

filesWidthLimit = 40

def consolidateFiles(files):
	"""Given a <files> element, find the directory common to all files
	   and return a 2-tuple with that directory followed by
	   a list of files within that directory.
	   """
	# If we only have one file, return it as the prefix.
	# This prevents the below regex from deleting the filename
	# itself, assuming it was a partial filename.
	if len(files) == 1:
		return files[0], []

	# Start with the prefix found by commonprefix,
	# then actually make it end with a directory rather than
	# possibly ending with part of a filename.
	prefix = re.sub("[^/]*$", "", posixpath.commonprefix(files))

	endings = []
	for file in files:
		ending = file[len(prefix):].strip()
		if ending == '':
				ending = '.'
		endings.append(ending)
	return prefix, endings

def summarizeFiles(files):
	"""Given a list of strings representing file paths, return
	   a summary of those files and/or directories. This is used
	   in place of a full file list when that would be too long.
	   """
	# Count the number of distinct directories we have
	dirs = {}
	for file in files:
		dirs[posixpath.split(file)[0]] = True

	if len(dirs) <= 1:
		return "%d files" % len(files)
	else:
		return "%d files in %d dirs" % (len(files), len(dirs))

def handleFiles(files):
	"""Break up our list of files into a common prefix and a sensibly-sized
	   list of filenames after that prefix.
	   """
	prefix, endings = consolidateFiles(files)
	endingStr = " ".join(endings)
	if len(endingStr) > filesWidthLimit:
		# If the full file list is too long, give a file summary instead
		endingStr = summarizeFiles(endings)
	if prefix.startswith('/'):
		prefix = prefix[1:]

	if endingStr:
		return "%s (%s)" % (prefix, endingStr)
	else:
		return prefix

def sendCommit(commitstr, sockpath):
	xml = minidom.parseString(commitstr)
	author = saxutils.unescape(xml.getElementsByTagName('author')[0].firstChild.toxml())
	files = []
	for i in xml.getElementsByTagName('file'):
		files.append(saxutils.unescape(i.firstChild.toxml()))
	module = saxutils.unescape(xml.getElementsByTagName('module')[0].firstChild.toxml())
	log = saxutils.unescape(xml.getElementsByTagName('log')[0].firstChild.toxml()).replace('&quot;', r'\"')
	lines = []
	lines.append("03%s * 10%s/%s:" % (author, module, handleFiles(files)))
	lines.extend(log.split('\n'))

	client = socket.socket ( socket.AF_UNIX, socket.SOCK_DGRAM )
	client.connect (sockpath)
	client.send ("\n".join(["""c.privmsg("#frugalware.dev", "%s")""" % i for i in lines]))
	client.close()
