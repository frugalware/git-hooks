#!/usr/bin/env python

import os

class config:
	project = "Frugalware"
	# just set this to None if you don't need this
	gitweb_url = "http://git.frugalware.org"
	rpc_uri = "http://cia.vc"
	# if false, then the mail will be printed to stdout and no xml-rpc post
	# will be performed
	post = False
