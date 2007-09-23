#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

import os, xmlrpclib, timeoutsocket, cgi
from xml.sax import saxutils
from config import config

__version__ = "0.1.0"
__url__ = "http://ftp.frugalware.org/pub/other/git-hooks"

def unaccent(s):
	ret = []
	fro = "������������������"
	to = "AEIOOOUUUaeiooouuu"
	for i in s:
		if i in fro:
			ret.append(to[fro.index(i)])
		else:
			ret.append(i)
	return "".join(ret)

def readfrompipe(cmd):
	sock = os.popen(cmd)
	ret = sock.read().strip()
	sock.close()
	return ret

def callback(patch):
	global config
	repo = os.getcwd().split("/")[-1]
	if repo == ".git":
		repo = os.getcwd().split("/")[-2]
	url = ""
	if config.gitweb_url:
		url = "<url>%s?p=%s.git;a=commitdiff;h=%s</url>" % (config.gitweb_url, repo, patch)
	refname = "master"
	rev = patch[:12]
	raw = readfrompipe("git cat-file commit " + patch)
	for i in raw.split("\n"):
		if i.startswith("author "):
			author = cgi.escape(unaccent(" ".join(i[len("author "):].split(" ")[:-2])))
			ts = i[len("author "):].split(" ")[-2]
	logmessage = cgi.escape("\n\n".join(raw.split("\n\n")[1:]))
	files = []
	for i in readfrompipe("git diff-tree -r --name-only " + patch).split("\n")[1:]:
		files.append("<file>%s</file>" % i.strip())

	msg = """<?xml version="1.0" ?>
<message>
	<generator>
		<name>CIA plugin for git-hooks.py</name>
		<version>%(version)s</version>
		<url>%(url)s</url>
	</generator>
	<source>
		<project>%(project)s</project>
		<module>%(module)s</module>
	</source>
	<timestamp>%(timestamp)s</timestamp>
	<body>
		<commit>
			<author>%(author)s</author>
			<!-- <revision>%(revision)s</revision> -->
			<files>
				%(files)s
			</files>
			<log>%(log)s</log>
			%(purl)s
		</commit>
	</body>
</message>
	""" % {
		'version': __version__,
		'url': __url__,
		'project': config.project,
		'module': repo,
		'timestamp': ts,
		'author': author,
		'revision': rev,
		'files': "\n".join(files),
		'log': logmessage,
		'purl': url
	}

	if config.post:
		timeoutsocket.setDefaultSocketTimeout(20)
		try:
			xmlrpclib.ServerProxy(config.rpc_uri).hub.deliver(msg)
		except timeoutsocket.Timeout:
			print "Not notifying CIA, connection timed out."
		except Exception, s:
			print "Can't notify CIA (%s)" % s
	else:
		print msg
