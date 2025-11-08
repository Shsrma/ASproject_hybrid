import requests
import json

JAVA_BASE = "http://127.0.0.1:9000"

def verify_blockchain(block_data):
    try:
        resp = requests.post(JAVA_BASE + "/verify", json={"block": block_data}, timeout=5)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def get_timezone_info(region=None):
    try:
        params = {}
        if region:
            params['region'] = region
        resp = requests.get(JAVA_BASE + "/timezone", params=params, timeout=5)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def translate(text, lang='en'):
    try:
        params = {'lang': lang, 'text': text}
        resp = requests.get(JAVA_BASE + "/translate", params=params, timeout=5)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
