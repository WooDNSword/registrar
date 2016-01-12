import json

# TODO: Document read_cfg.
def read_cfg(file_path):
	with open(file_path) as f:
		return json.loads(f.read())
