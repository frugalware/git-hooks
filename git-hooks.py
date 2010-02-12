#!/usr/bin/env python

import os, sys

sys = reload(sys)
sys.setdefaultencoding("utf-8")

def run_hook(callback, old, new, ref):
	if old == "0000000000000000000000000000000000000000":
		sys.exit(0)
	ret = os.system("git rev-parse -q --verify %s^2 >/dev/null" % new)
	if ret == 0:
		merge = True
	else:
		merge = False

	sock = os.popen("git rev-list %s..%s" % (old, new))
	hashes = sock.readlines()
	sock.close()
	hashes.reverse()

	for i in hashes:
		# the second parameter is true, if this is a commit of a
		# merge (ie. if it's true, then the sendmail script
		# won't send it out, so that only the merge commit is
		# mailed after a merge)
		last = i == hashes[-1]
		callback(i.strip(), merge and not last, ref)

if __name__ == "__main__":
	sys.path.append("/etc/git-hooks")
	sys.path.append("/usr/share/git-hooks")
	from config import config as myconfig
	for line in sys.stdin.readlines():
		(old, new, ref) = line.split(' ')
		name = sys.argv[0].split('/')[1]
		if name == "home":
			name = "post-receive"
		for i in myconfig.enabled_plugins[name]:
			s = "%s.%s" % (i, i)
			plugin = __import__(s)
			for j in s.split(".")[1:]:
				plugin = getattr(plugin, j)
			try:
				run_hook(plugin.callback, old, new, ref)
			except Exception, s:
					print "Can't run plugin '%s' (%s)" % (i, s)
