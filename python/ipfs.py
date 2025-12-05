import os
import requests
import shutil


class IPFSClient:
    def __init__(self):
        """
        Uses IPFS_HOST environment variable when deployed.
        Default: local IPFS daemon (http://127.0.0.1:5001)
        """
        self.host = os.environ.get("IPFS_HOST", "http://127.0.0.1:5001")

    def upload_file(self, file_path):
        """
        Upload a file to IPFS using the HTTP API.
        Returns the CID (hash).
        """
        url = f"{self.host}/api/v0/add"
        with open(file_path, "rb") as f:
            response = requests.post(url, files={"file": f})
        response.raise_for_status()
        return response.json()["Hash"]

    def download_file(self, ipfs_hash, download_folder):
        """
        Download a file from IPFS and save it to a folder.
        Returns the final downloaded file path.
        """
        url = f"{self.host}/api/v0/get?arg={ipfs_hash}"

        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        temp_path = os.path.join(download_folder, ipfs_hash + ".tar")

        # Download content
        response = requests.post(url, stream=True)
        response.raise_for_status()

        with open(temp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Extract content
        extract_dir = os.path.join(download_folder, ipfs_hash)
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)

        shutil.unpack_archive(temp_path, extract_dir, format="tar")
        os.remove(temp_path)

        # Return first file in the extracted folder
        for root, _, files in os.walk(extract_dir):
            if files:
                return os.path.join(root, files[0])

        raise FileNotFoundError("No files found in IPFS download.")
