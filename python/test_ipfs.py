from ipfs import IPFSClient

ipfs = IPFSClient()
cid = ipfs.upload_file("sample.txt")
print("CID:", cid)
