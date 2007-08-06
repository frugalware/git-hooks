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

def tobuild(pkg):
	ret = []
	# Build the command to read the FrugalBuilds
	command = 'source /usr/lib/frugalware/fwmakepkg'
	command += ' ; source %s'
	command += ' ; [ -n "${nobuild}" ] && exit'
	command += ' ; echo ${options[@]} | grep -q nobuild && exit'
	command += ' ; echo "${pkgname}-${pkgver}-${pkgrel}"'
	command += ' ; echo "${archs[@]}"'
	sock = os.popen(command % pkg)
	lines = sock.readlines()
	sock.close()
	if not len(lines):
		return ret
	archs = lines[1].strip().split()
	for i in archs:
		if i not in config.archs:
			continue
		full = "-".join([lines[0].strip(), i])
		try:
			os.stat("frugalware-%s/%s.fpm" % (i, full))
		except OSError:
			ret.append(full)
	return ret

def callback(patch):
	global config
	repo = os.getcwd().split("/")[-1]
	if repo == ".git":
		repo = os.getcwd().split("/")[-2]
	if repo not in config.repos:
		return
	server = xmlrpclib.Server(config.server_url)
	for i in readfrompipe("git diff-tree -r --name-only " + patch).split("\n")[1:]:
		if re.match("^source/[^/]+/[^/]+/FrugalBuild$", i):
			for j in tobuild(i):
				server.request_build(config.server_user, config.server_pass, "git://%s/%s" % (repo.replace("frugalware-", ""), j))
