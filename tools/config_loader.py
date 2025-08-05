import json

def load_crypto_config(path="tools/config.json") -> dict:
    with open(path, "r") as f:
        data = json.load(f)
        return data[0]