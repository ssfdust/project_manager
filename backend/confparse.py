import os
import json

def get_config(config_file='/etc/docker_manager/config.json'):
    if not os.path.exists(config_file):
        return None
    with open(config_file, 'r') as f:
        config = json.loads(f.read())
    return config

