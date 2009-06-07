#!/usr/bin/env python

import os, sys

sys = reload(sys)
sys.setdefaultencoding("utf-8")

def run_hook(callback, old, new):
	if old == "0000000000000000000000000000000000000000":
		sys.exit(0)
	ret = os.system("git rev-parse -q --verify %s^2 >/dev/null" % new)
	if ret == 0:
		# this is a merge, we just want to accounce the merge
		# commit
		callback(new.strip())
		return

	sock = os.popen("git rev-list %s..%s" % (old, new))
	hashes = sock.readlines()
	sock.close()
	hashes.reverse()

	for i in hashes:
		callback(i.strip())

def read_stdin():
	# currently we don't care about !master branches
	old = None
	for i in sys.stdin.readlines():
		(old, new, ref) = i.split(' ')
		if ref == "refs/heads/master":
			break
	if not old:
		sys.exit(1)
	return old, new


if __name__ == "__main__":
	sys.path.append("/etc/git-hooks")
	sys.path.append("/usr/share/git-hooks")
	from config import config as myconfig
	old, new = read_stdin()
	name = sys.argv[0].split('/')[1]
	if name == "home":
		name = "post-receive"
	for i in myconfig.enabled_plugins[name]:
		s = "%s.%s" % (i, i)
		plugin = __import__(s)
		for j in s.split(".")[1:]:
			plugin = getattr(plugin, j)
		try:
			run_hook(plugin.callback, old, new)
		except Exception, s:
				print "Can't run plugin '%s' (%s)" % (i, s)
