#!/usr/bin/env python

class config:
	enabled_plugins = {
			# "post-receive": ['sendmail'],
			"post-receive": ['checkout', 'synchook', 'cia'],
			"pre-receive": ['detach']
			}
