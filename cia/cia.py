#!/usr/bin/env python

import os, gzip, time, re, xmlrpclib, timeoutsocket
from xml.sax import saxutils
from config import config

__version__ = "0.1.0"
__url__ = "http://ftp.frugalware.org/pub/other/darcs-hooks"

def getpatch(hash):
	sock = gzip.GzipFile(os.path.join("_darcs", "patches", "%s") % hash)
	data = sock.readlines()
	sock.close()
	return data

def callback(patch):
	global config
	files = []
	repo = os.path.split(os.getcwd())[-1]
	patchname = patch.getElementsByTagName("name")[0].firstChild.toxml()
	try:
		patchlog = patch.getElementsByTagName("comment")[0].firstChild.toxml()
	except IndexError:
		patchlog = None
	hash = saxutils.unescape(patch.attributes['hash'].firstChild.toxml())
	if patchlog:
		log = "* %s\n%s" % (patchname, patchlog)
	else:
		log = "* %s" % patchname
	url = ""
	if config.darcsweb_url:
		url = "<url>%s?r=%s;a=darcs_commitdiff;h=%s;</url>" % (config.darcsweb_url, repo, hash)

	patchdata = getpatch(hash)
	for i in patchdata:
		i = i.strip().replace("./", "")
		if i.startswith("adddir "):
			files.append(re.sub(r"^adddir (.*)", r"\1", i))
		elif i.startswith("addfile "):
			files.append(re.sub(r"^addfile (.*)", r"\1", i))
		elif i.startswith("rmdir "):
			files.append(re.sub(r"^rmdir (.*)", r"\1", i))
		elif i.startswith("rmfile "):
			files.append(re.sub(r"^rmfile (.*)", r"\1", i))
		elif i.startswith("binary "):
			files.append(re.sub(r"^binary (.*)", r"\1", i))
		elif i.startswith("hunk "):
			files.append(re.sub(r"^hunk (.*) [0-9]+", r"\1", i))
		elif i.startswith("move "):
			files.append(re.sub(r"^move (.*) .*", r"\1", i))
			files.append(re.sub(r"^move .* (.*)", r"\1", i))
	# remove duplicates. it does not preserve the order but that's not a
	# problem here
	set = {}
	map(set.__setitem__, files, [])
	files = set.keys()

	msg = """<?xml version="1.0" ?>
<message>
	<generator>
		<name>CIA plugin for for darcs-hooks.py</name>
		<version>%(version)s</version>
		<url>http://ftp.frugalware.org/pub/other/darcs-hooks</url>
	</generator>
	<source>
		<project>%(project)s</project>
		<module>%(module)s</module>
	</source>
	<timestamp>%(timestamp)s</timestamp>
	<body>
		<commit>
			<author>%(author)s</author>
			<files>
				<file>%(files)s</file>
			</files>
			<log>%(log)s</log>
			%(url)s
		</commit>
	</body>
</message>
	""" % {
		'version': __version__,
		'project': config.project,
		'module': repo,
		'timestamp': str(int(time.time())),
		'author': patch.attributes['author'].firstChild.toxml(),
		'files': "</file>\n<file>".join(files),
		'log': log,
		'url': url
	}

	if config.post:
		timeoutsocket.setDefaultSocketTimeout(20)
		xmlrpclib.ServerProxy(config.rpc_uri).hub.deliver(msg)
	else:
		print msg

if __name__ == "__main__":
	hook = Hook(config.dir, config.latestfile, sendpatch)
