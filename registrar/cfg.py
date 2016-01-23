# TODO: Document the module!
# TODO: Move this module into an independent repository (DRY principle: more
# than one repository uses equivalent code.

import json

# TODO: Document readCfg.
def readCfg(file_path):
	with open(file_path) as f:
		return json.loads(f.read())
