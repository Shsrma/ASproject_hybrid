from flask import Flask, request, render_template, send_file, jsonify
import os
from ipfs import IPFSClient
from blockchain import Blockchain
from api_bridge import verify_blockchain, get_timezone_info, translate

app = Flask(__name__, template_folder="templates")

# -------------------------
# Load IPFS + Blockchain
# -------------------------
ipfs_client = IPFSClient()

# No file save → cloud-safe
blockchain = Blockchain()  

# -------------------------
# Directories
# -------------------------
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
DOWNLOAD_FOLDER = os.environ.get("DOWNLOAD_FOLDER", "downloads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# -------------------------
# ROUTES
# -------------------------
@app.route("/")
def index():
    return render_template("index.html", default_lang="en", default_theme="light")

# -------------------------
# File Upload → IPFS → Blockchain
# -------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file field found"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save locally
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Upload to IPFS
    try:
        ipfs_hash = ipfs_client.upload_file(file_path)
    except Exception as e:
        return jsonify({"error": f"IPFS upload failed: {str(e)}"}), 500

    # Store in blockchain (your FIXED blockchain)
    blockchain.create_block({
        "file_name": file.filename,
        "ipfs_hash": ipfs_hash
    })

    # Call Java Verify Service
    verify_result = verify_blockchain({
        "file_name": file.filename,
        "ipfs_hash": ipfs_hash
    })

    return jsonify({
        "message": "File uploaded successfully",
        "ipfs_hash": ipfs_hash,
        "verify": verify_result
    })

# -------------------------
# File Download From IPFS
# -------------------------
@app.route("/download", methods=["POST"])
def download_file():
    ipfs_hash = request.form.get("ipfs_hash")
    if not ipfs_hash:
        return jsonify({"error": "No IPFS hash provided"}), 400

    # Lookup original name in blockchain
    original_filename = None
    for block in blockchain.chain:
        if isinstance(block.data, dict) and block.data.get("ipfs_hash") == ipfs_hash:
            original_filename = block.data["file_name"]
            break

    if not original_filename:
        return jsonify({"error": "Hash not found in blockchain"}), 404

    # Download from IPFS
    try:
        downloaded_path = ipfs_client.download_file(ipfs_hash, DOWNLOAD_FOLDER)
    except Exception as e:
        return jsonify({"error": f"IPFS download failed: {str(e)}"}), 500

    if not downloaded_path or not os.path.exists(downloaded_path):
        return jsonify({"error": "Downloaded file not found"}), 500

    # Final rename
    final_path = os.path.join(DOWNLOAD_FOLDER, original_filename)

    if os.path.isdir(downloaded_path):
        files = os.listdir(downloaded_path)
        if not files:
            return jsonify({"error": "IPFS returned an empty folder"}), 500
        source = os.path.join(downloaded_path, files[0])
    else:
        source = downloaded_path

    if os.path.exists(final_path):
        os.remove(final_path)

    os.replace(source, final_path)

    return send_file(final_path, as_attachment=True, download_name=original_filename)

# -------------------------
# Java Microservice Routes
# -------------------------
@app.route("/timezone-info")
def timezone_info():
    region = request.args.get("region")
    return jsonify(get_timezone_info(region))

@app.route("/translate-ui")
def translate_ui():
    text = request.args.get("text", "Hello")
    lang = request.args.get("lang", "en")
    return jsonify(translate(text, lang))

# -------------------------
# App Runner
# -------------------------
if __name__ == "__main__":
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"

    app.run(host=host, port=port, debug=debug)
