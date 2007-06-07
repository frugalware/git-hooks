#!/usr/bin/env python

import os

class config:
	dir = os.path.join("_darcs", "third_party", "email")
	latestfile = "latest"
	dest = "frugalware-darcs@frugalware.org"
	# just set this to None if you don't need this
	darcsweb_url = "http://darcs.frugalware.org/darcsweb/darcsweb.cgi"
	# if false, then the mail will be printed to stdout and no mail will be
	# sent
	send = True
