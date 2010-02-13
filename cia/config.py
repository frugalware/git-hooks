#!/usr/bin/env python

import os

class config:
	project = "Frugalware"
	# just set this to None if you don't need this
	gitweb_url = "http://git.frugalware.org/gitweb/gitweb.cgi"
	rpc_uri = "http://cia.vc"
	# if false, then the mail will be printed to stdout and no xml-rpc post
	# will be performed
	post = True
	sockpath = "/home/ftp/pub/other/people/vmiklos/mxw/mxw2.sock"
	timeout = 3
