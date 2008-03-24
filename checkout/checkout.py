#!/usr/bin/env python

import os, time, sys

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
			sys.stdout.flush()
			time.sleep(1)
		except OSError:
			ret = os.system("git symbolic-ref HEAD &>/dev/null")
			if ret != 0:
				# this is a detached head
				os.system("git checkout -m master 2>/dev/null")
			else:
				# we don't know where we are, need to
				# check every checked out file
				os.system("git checkout -f")
			return
	print "WARNING: Timeout exceeded, checkout failed!"
