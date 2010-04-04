#!/usr/bin/env python

import os, time, sys

first = True

def callback(patch, merge, ref):
	global first

	if not first:
		return
	if ref != "refs/heads/master":
		return
	first = False
	cwd = os.getcwd()
	os.chdir("..")
	if "GIT_DIR" in os.environ.keys():
		del os.environ['GIT_DIR']
	limit = 300
	for i in range(limit):
		try:
			os.stat(".git/index.lock")
			print "Waiting for lock to be released to do a 'git checkout'"
			sys.stdout.flush()
			time.sleep(1)
		except OSError:
			sock = os.popen("git show-ref -h -s HEAD")
			hash = sock.readline().strip()
			sock.close()
			os.system("git checkout -m %s 2>/dev/null" % hash)
			os.chdir(cwd)
			return
	print "WARNING: Timeout exceeded, checkout failed!"
	os.chdir(cwd)
