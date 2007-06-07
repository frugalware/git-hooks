#!/usr/bin/env python

import os, gzip, time, re, xmlrpclib
from xml.dom import minidom
from xml.sax import saxutils

class Hook:
	def __init__(self, dir, latestfile, callback):
		self.dir = dir
		self.latestfile = latestfile
		self.callback = callback

		try:
			os.stat(dir)
		except OSError:
			os.makedirs(dir)

		try:
			sock = open(os.path.join(self.dir, self.latestfile), "r")
		except IOError:
			sock = None

		if not sock:
			xmldoc = self.getxml("darcs chan --last 1 --xml-output")

			hash = xmldoc.getElementsByTagName('patch')[0].attributes['hash'].firstChild.toxml()
			self.puthash(hash)
		else:
			oldhash = sock.read().strip()
			sock.close()

			xmldoc = self.getxml('darcs chan --from-match "hash %s" --xml-output' % oldhash)

			counter = 0
			for i in xmldoc.getElementsByTagName('patch'):
				if counter >= len(xmldoc.getElementsByTagName('patch'))-1:
					break
				self.callback(i)
				counter += 1

			hash = xmldoc.getElementsByTagName('patch')[0].attributes['hash'].firstChild.toxml()
			self.puthash(hash)

	def getxml(self, cmd):
		sock = os.popen(cmd)
		xmldata = "".join(sock.readlines())
		sock.close()
		xmldoc = minidom.parseString(xmldata)
		return xmldoc

	def puthash(self, hash):
		sock = open(os.path.join(self.dir, self.latestfile), "w")
		sock.write("%s\n" % hash)
		sock.close()

if __name__ == "__main__":
	from sendmail.sendmail import config
	from sendmail.sendmail import callback
	hook = Hook(config.dir, config.latestfile, callback)
