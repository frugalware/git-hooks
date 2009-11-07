#!/usr/bin/env python

class config:
	enabled_plugins = {
			"post-receive": ['sendmail', 'checkout', 'synchook', 'cia'],
			"pre-receive": ['detach']
			}
