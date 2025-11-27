import os
import ipfshttpclient

import shutil


class IPFSClient:
    def __init__(self):
        """
        Use environment variable IPFS_HOST for cloud compatibility.
        Defaults to local IPFS daemon: 127.0.0.1:5001
        """
        ipfs_host = os.environ.get("IPFS_HOST", "/ip4/127.0.0.1/tcp/5001")

        try:
            self.client = ipfshttpclient.connect(ipfs_host)
        except Exception as e:
            raise RuntimeError(f"Unable to connect to IPFS at {ipfs_host}: {e}")

    def upload_file(self, file_path):
        """
        Upload a file to IPFS.
        Handles both old-style and list-style responses.
        """
        res = self.client.add(file_path)

        # Handle response types
        if isinstance(res, list):  # newer versions return list of dicts
            res = res[-1]

        return res.get("Hash")

    def download_file(self, ipfs_hash, download_folder):
        """
        Download a file/folder from IPFS.
        Ensures clean folder, handles different IPFS output formats.
        """
        target_path = os.path.join(download_folder, ipfs_hash)

        # Ensure base folder exists
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Clean previous download for same hash
        if os.path.exists(target_path):
            shutil.rmtree(target_path)

        # Fetch from IPFS
        self.client.get(ipfs_hash, target=download_folder)

        # Check if IPFS created a folder named after the hash
        if os.path.isdir(target_path):
            # Return the first file inside the hash folder
            for root, _, files in os.walk(target_path):
                if files:
                    return os.path.join(root, files[0])

        # If a single file was downloaded directly
        direct_file = os.path.join(download_folder, ipfs_hash)
        if os.path.isfile(direct_file):
            return direct_file

        # If get created multiple items, return first file found
        for item in os.listdir(download_folder):
            item_path = os.path.join(download_folder, item)
            if os.path.isfile(item_path):
                return item_path

        raise FileNotFoundError("Downloaded IPFS content contains no files.")

