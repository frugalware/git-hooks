#!/usr/bin/env python

import os, time, sys, glob

first = True

def callback(patch, merge):
	global first

	if merge:
		return

	timeout = True
	if first:
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
					os.system(r"git checkout -m $(git log -g -1|grep 'moving from'|sed 's/.*from \(.*\) to .*/\1/') 2>/dev/null")
				else:
					# we don't know where we are, need to
					# check every checked out file
					os.system("git checkout -f")
				timeout = False
				break
		if timeout:
			print "WARNING: Timeout exceeded, checkout failed!"

	# now handle pkg renames
	sock = os.popen("git diff-tree -r %s -M --name-status --diff-filter=R" % patch)
	renames = sock.read().strip()
	sock.close()
	pkgmove = False
	for i in renames.split('\n'):
		if len(i.split('\t')) < 2:
			continue
		fro, to = i.split('\t')[1:]
		if os.path.split(fro)[1] != "FrugalBuild":
			continue
		pkgmove = True
		frodir = os.path.sep.join(fro.split(os.path.sep)[1:-1])
		todir = os.path.sep.join(to.split(os.path.sep)[1:-1])
		break
	if pkgmove:
		os.chdir("source")
		for i in glob.glob(frodir+os.path.sep+"*"):
			tofile = os.path.join(todir, os.path.split(i)[1])
			print "Moving untracked file: %s -> %s" % (i, tofile)
			os.rename(i, tofile)
		print "Removing empty dir %s" % frodir
		os.rmdir(frodir)

if __name__ == "__main__":
	os.chdir("/home/vmiklos/git/current/.git")
	sock = os.popen("git rev-list -1 HEAD")
	patch = sock.readline().strip()
	sock.close()
	callback(patch, False)
