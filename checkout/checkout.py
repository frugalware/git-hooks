#!/usr/bin/env python

import os

first = True

def callback(patch):
	global first

	if not first:
		return
	first = False
	os.chdir("..")
	if "GIT_DIR" in os.environ.keys():
		del os.environ['GIT_DIR']
	os.system("git checkout -f")
