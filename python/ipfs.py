# ipfs.py
import os
import requests
import shutil


class IPFSClient:
    def __init__(self):
        self.host = os.environ.get("IPFS_HOST", "http://127.0.0.1:5001")

    def upload_file(self, file_path):
        url = f"{self.host}/api/v0/add"
        with open(file_path, "rb") as f:
            response = requests.post(url, files={"file": f})
        response.raise_for_status()
        return response.json()["Hash"]

    def download_file(self, ipfs_hash, download_folder):
        """
        Works correctly with IPFS 0.39.0 (no TAR)
        """
        url = f"{self.host}/api/v0/cat?arg={ipfs_hash}"

        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        final_path = os.path.join(download_folder, ipfs_hash)

        response = requests.post(url, stream=True)
        response.raise_for_status()

        with open(final_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        return final_path
