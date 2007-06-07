#!/usr/bin/env python

import os, gzip, smtplib
from xml.dom import minidom
from xml.sax import saxutils
from config import config

def getpatch(hash):
	sock = gzip.GzipFile(os.path.join("_darcs", "patches", "%s") % hash)
	data = "".join(sock.readlines())
	sock.close()
	return data

def callback(patch):
	global config
	msg = []
	repo = os.path.split(os.getcwd())[-1]
	patchname = patch.getElementsByTagName("name")[0].firstChild.toxml()
	hash = saxutils.unescape(patch.attributes['hash'].firstChild.toxml())

	fro = saxutils.unescape(patch.attributes['author'].firstChild.toxml())
	to = config.dest
	subject = "%s: %s" % (repo, patchname)
	msg.append("From: %s \nTo: %s\nSubject: %s\n" % (fro, to, subject))

	if config.darcsweb_url:
		msg.append("Darcsweb-Url: %s?r=%s;a=darcs_commitdiff;h=%s;\n" % (config.darcsweb_url, repo, hash))
	msg.append(getpatch(hash))

	if config.send:
		server = smtplib.SMTP('localhost')
		server.sendmail(fro, to, "\n".join(msg))
		server.quit()
	else:
		print "\n".join(msg)

if __name__ == "__main__":
	hook = Hook(config.dir, config.latestfile, sendpatch)
