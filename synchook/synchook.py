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
	ret = s
	rep = {"\xc1":"A", "\xc9":"E", "\xcd":"I", "\xd3":"O", "\xd6":"O", "\xd5":"O", "\xda":"U", "\xdc":"U", "\xdb":"U", "\xe1":"a", "\xe9":"e", "\xed":"i", "\xf3":"o", "\xf6":"o", "\xf5":"o", "\xfa":"u", "\xfc":"u", "\xfb":"u",
			"\xc3\x81":"A", "\xc3\x89":"E", "\xc3\x8d":"I", "\xc3\x93":"O", "\xc3\x96":"O", "\xc5\x90":"O", "\xc3\x9a":"U", "\xc3\x9c":"U", "\xc5\xb0":"U", "\xc3\xa1":"a", "\xc3\xa9":"e", "\xc3\xad":"i", "\xc3\xb3":"o", "\xc3\xb6":"o", "\xc5\x91":"o", "\xc3\xba":"u", "\xc3\xbc":"u", "\xc5\xb1":"u"}
	for k, v in rep.items():
		ret = ret.replace(k, v)
	return ret

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
				repo = repo.replace(os.readlink("/pub/frugalware/frugalware-stable").split('-')[1], "stable")
				server.request_build(config.server_user, config.server_pass, "git://%s/%s/%s" % (repo, j, unaccent(author)))

if __name__ == "__main__":
	os.chdir("/home/vmiklos/git/current")
	sock = os.popen("git rev-list -1 HEAD")
	patch = sock.readline().strip()
	sock.close()
	callback(patch)
