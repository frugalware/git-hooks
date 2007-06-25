#!/usr/bin/env python

import os

first = True

def callback(patch):
	global first

	if not first:
		return
	first = True
	os.chdir("..")
	del os.environ['GIT_DIR']
	os.system("git checkout -f")
