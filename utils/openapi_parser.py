import yaml
import json
import random
import string

def load_spec(filepath):
    with open(filepath) as f:
        if filepath.endswith('.yaml') or filepath.endswith('.yml'):
            return yaml.safe_load(f)
        return json.load(f)

def generate_test_data(schema):
    if not schema:
        return None
    if schema.get('type') == 'string':
        return ''.join(random.choices(string.ascii_letters, k=10))
    elif schema.get('type') == 'integer':
        return random.randint(1, 100)
    elif schema.get('type') == 'boolean':
        return random.choice([True, False])
    elif schema.get('type') == 'object':
        return {k: generate_test_data(v) for k, v in schema.get('properties', {}).items()}
    elif schema.get('type') == 'array':
        return [generate_test_data(schema.get('items', {})) for _ in range(3)]
    return None