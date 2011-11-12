#!/usr/bin/env python

import os

class config:
	dest = "frugalware-git@frugalware.org"
	# just set this to None if you don't need this
	gitweb_url = "http://git.frugalware.org/gitweb/gitweb.cgi"
	# if false, then the mail will be printed to stdout and no mail will be
	# sent
	send = True
