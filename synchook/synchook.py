#!/usr/bin/env python

import os, xmlrpclib, re
from config import config

__version__ = "0.1.0"
__url__ = "http://ftp.frugalware.org/pub/other/git-hooks"

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
	if repo not in config.repos:
		return
	pkgs = []
	for i in readfrompipe("git diff-tree -r --name-only " + patch).split("\n")[1:]:
		if re.match("^source/[^/]+/[^/]+/FrugalBuild$", i):
			pkgs.append(i.split('/')[-2])
	# TODO: xmlrpc call missing here
