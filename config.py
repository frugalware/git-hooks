#!/usr/bin/env python

class config:
	enabled_plugins = {
			"post-receive": ['cia', 'sendmail', 'checkout', 'synchook'],
			"pre-receive": ['detach']
			}
