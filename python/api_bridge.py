# api_bridge.py
import requests
import os

JAVA_BASE = os.environ.get("JAVA_API", "http://127.0.0.1:9000")


def verify_blockchain(block_data):
    try:
        resp = requests.post(
            f"{JAVA_BASE}/verify",
            json={"block": block_data},
            timeout=5
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": f"Java verify unreachable: {str(e)}"}


def get_timezone_info(region=None):
    try:
        params = {}
        if region:
            params["region"] = region

        resp = requests.get(f"{JAVA_BASE}/timezone", params=params, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": f"Java timezone unreachable: {str(e)}"}


def translate(text, lang="en"):
    try:
        params = {"text": text, "lang": lang}
        resp = requests.get(f"{JAVA_BASE}/translate", params=params, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": f"Java translate unreachable: {str(e)}"}
