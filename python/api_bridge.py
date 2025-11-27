import requests
import os

# Allow overriding Java microservice URL (cloud safe)
JAVA_BASE = os.environ.get("JAVA_API", "http://127.0.0.1:9000")


def verify_blockchain(block_data):
    """
    Sends a block to the Java verification service.
    """
    try:
        resp = requests.post(
            f"{JAVA_BASE}/verify",
            json={"block": block_data},
            timeout=5
        )
        return resp.json()
    except Exception as e:
        return {"error": f"Java verify service unreachable: {str(e)}"}


def get_timezone_info(region=None):
    """
    Get timezone information from Java microservice.
    """
    try:
        params = {}
        if region:
            params['region'] = region

        resp = requests.get(
            f"{JAVA_BASE}/timezone",
            params=params,
            timeout=5
        )
        return resp.json()
    except Exception as e:
        return {"error": f"Java timezone service unreachable: {str(e)}"}


def translate(text, lang='en'):
    """
    Translate UI text using Java microservice.
    """
    try:
        params = {"text": text, "lang": lang}

        resp = requests.get(
            f"{JAVA_BASE}/translate",
            params=params,
            timeout=5
        )
        return resp.json()
    except Exception as e:
        return {"error": f"Java translate service unreachable: {str(e)}"}
