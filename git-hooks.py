#!/usr/bin/env python

import os, sys

class Hook:
	def __init__(self, callback):

		# currently we don't care about !master branches
		old = None
		for i in sys.stdin.readlines():
			(old, new, ref) = i.split(' ')
			if ref == "refs/heads/master":
				break
		if not old:
			return

		sock = os.popen("git rev-list %s..%s" % (old, new))
		hashes = sock.readlines()
		sock.close()
		hashes.reverse()

		for i in hashes:
			callback(i.strip())

if __name__ == "__main__":
	sys.path.append("/etc/git-hooks")
	sys.path.append("/usr/share/git-hooks")
	from config import config as myconfig
	for i in myconfig.enabled_plugins:
		s = "%s.%s" % (i, i)
		plugin = __import__(s)
		for j in s.split(".")[1:]:
			plugin = getattr(plugin, j)
		s = "%s.config" % i
		config = __import__(s)
		for j in s.split(".")[1:]:
			config = getattr(config, j)
		#try:
		hook = Hook(plugin.callback)
		#except Exception, s:
		#	print "Error, probably connect to CIA timed out."
