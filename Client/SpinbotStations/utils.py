import yaml
import re

def _clean_yaml(data: dict) -> dict:
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            if value == '':
                continue
            if isinstance(value, dict):
                cleaned_value = _clean_yaml(value)
                if cleaned_value:
                    cleaned[key] = cleaned_value
            else:
                cleaned[key] = value
        return cleaned
    return data

def parse_yaml(filename: str) -> dict:
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    
    return _clean_yaml(data)

def sort_steps(filename: str) -> dict:
    data = parse_yaml(filename)
    def step_num(key):
        match = re.search(r'(\d+)', key)
        return int(match.group(1)) if match else float('inf')
    return dict(sorted(data.items(), key=lambda item: step_num(item[0])))