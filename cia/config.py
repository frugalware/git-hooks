#!/usr/bin/env python

import os

class config:
	dir = os.path.join("_darcs", "third_party", "cia")
	latestfile = "latest"
	project = "Frugalware"
	# just set this to None if you don't need this
	darcsweb_url = "http://darcs.frugalware.org/darcsweb/darcsweb.cgi"
	rpc_uri = "http://cia.vc"
	# if false, then the mail will be printed to stdout and no xml-rpc post
	# will be performed
	post = False
