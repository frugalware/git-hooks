#!/usr/bin/env python

import os, time

first = True

def callback(patch):
	global first

	if not first:
		return
	first = False
	os.chdir("..")
	if "GIT_DIR" in os.environ.keys():
		del os.environ['GIT_DIR']
	limit = 300
	for i in range(limit):
		try:
			os.stat(".git/index.lock")
			print "Waiting for lock to be released to do a 'git checkout'"
			time.sleep(1)
		except OSError:
			os.system("git checkout -f")
			return
	print "WARNING: Timeout exceeded, checkout failed!"
