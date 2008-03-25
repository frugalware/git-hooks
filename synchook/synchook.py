#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

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
	try:
		os.stat(pkg)
	except OSError:
		return ret
	# Build the command to read the FrugalBuilds
	command = 'cd %s'
	command += ' ; source /usr/lib/frugalware/fwmakepkg'
	command += ' ; source FrugalBuild'
	command += ' ; [ -n "${nobuild}" ] && exit'
	command += ' ; nobuild=0 ; if echo ${options[@]} | grep -q nobuild'
	command += ' ; then i=0 ; for subpkg in "${subpkgs[@]}"'
	command += ' ; do echo ${suboptions[$i]} | grep -q nobuild || break; nobuild=1'
	command += ' ; done'
	command += ' ; [ "${#subpkgs[@]}" == 0 ] && nobuild=1'
	command += ' ; fi'
	command += ' ; [ $nobuild == 1 ] && exit'
	command += ' ; echo "${pkgname}-${pkgver}-${pkgrel}"'
	command += ' ; echo "${archs[@]}"'
	sock = os.popen(command % os.path.split(pkg)[0])
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

def unaccent(s):
	ret = []
	fro = "ÁÉÍÓÖŐÚÜŰáéíóöőúüű"
	to = "AEIOOOUUUaeiooouuu"
	for i in s:
		if i in fro:
			ret.append(to[fro.index(i)])
		else:
			ret.append(i)
	return "".join(ret)

def callback(patch):
	global config
	repo = os.getcwd().split("/")[-1]
	if repo == ".git":
		repo = os.getcwd().split("/")[-2]
	if repo not in config.repos:
		return
	server = xmlrpclib.Server(config.server_url)
	author = readfrompipe('git show --pretty=format:"%an <%ae>" ' + patch).split("\n")[0]
	for i in readfrompipe("git diff-tree -r --name-only " + patch).split("\n")[1:]:
		if re.match("^source/[^/]+/[^/]+/FrugalBuild$", i):
			for j in tobuild(i):
				repo = repo.replace("frugalware-", "")
				# hardwiring this is ugly
				repo = repo.replace("0.8", "stable")
				server.request_build(config.server_user, config.server_pass, "git://%s/%s/%s" % (repo, j, unaccent(author)))

if __name__ == "__main__":
	os.chdir("/home/vmiklos/git/current")
	sock = os.popen("git rev-list -1 HEAD")
	patch = sock.readline().strip()
	sock.close()
	callback(patch)
