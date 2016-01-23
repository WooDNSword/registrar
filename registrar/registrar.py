#!/usr/bin/env python
# TODO: Document the module!

import cfg
import conn
import os

if __name__ == '__main__':
	# TODO: Move cfg loading logic into a separate module/repo (exists in both
	# registrar and registrant).
	# os.path module shit deals with Python's idiotic file path mechanisms.
	cfg_data = cfg.readCfg(
		os.path.dirname(
			os.path.realpath(__file__)
		) + '/res/json/cfg.json'
	)
	
	globs = {
		'cfg': cfg_data,
		'clients': {}
	}
	
	conn.initiate(globs)
