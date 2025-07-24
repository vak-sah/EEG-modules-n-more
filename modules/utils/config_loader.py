import yaml
import copy

def load_config(path: str):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def update_config(base_config: dict, overrides: dict):
    new_config = copy.deepcopy(base_config)
    for key, val in overrides.items():
        if isinstance(val, dict) and key in new_config:
            new_config[key].update(val)
        else:
            new_config[key] = val
    return new_config