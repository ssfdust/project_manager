import os
import json

def get_config(config_file='/etc/docker_manager/config.json'):
    with open(config_file, 'r') as f:
        config = json.loads(f.read())
    return config
