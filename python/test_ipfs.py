# test_ipfs.py
from ipfs import IPFSClient

ipfs = IPFSClient()

try:
    cid = ipfs.upload_file("sample.txt")
    print("Upload CID:", cid)

    path = ipfs.download_file(cid, "downloads")
    print("Downloaded file path:", path)
except Exception as e:
    print("IPFS Error:", e)
