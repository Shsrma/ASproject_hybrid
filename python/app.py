# app.py

from flask import Flask, request, render_template, send_file, jsonify
import os
from ipfs import IPFSClient
from blockchain import Blockchain
from api_bridge import verify_blockchain, get_timezone_info, translate
from werkzeug.utils import secure_filename

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

# ----------------------------------------
# Folders
# ----------------------------------------
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
DOWNLOAD_FOLDER = os.environ.get("DOWNLOAD_FOLDER", "downloads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ----------------------------------------
# Core objects
# ----------------------------------------
ipfs_client = IPFSClient()
blockchain = Blockchain()


# ============================================================
# HOME PAGE  (Fixes 405 Error)
# ============================================================
@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        default_lang="en",
        default_theme="light"
    )


# ============================================================
# UPLOAD  (POST only)
# ============================================================
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save file locally
    safe_name = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, safe_name)
    file.save(file_path)

    # Upload to IPFS
    try:
        ipfs_hash = ipfs_client.upload_file(file_path)
    except Exception as e:
        return jsonify({"error": f"IPFS upload failed: {str(e)}"}), 500

    # Add to blockchain
    block_data = {
        "file_name": safe_name,
        "ipfs_hash": ipfs_hash
    }
    blockchain.create_block(block_data)

    # Ask Java to verify
    verify_result = verify_blockchain(block_data)

    return jsonify({
        "message": "Upload successful",
        "ipfs_hash": ipfs_hash,
        "verify": verify_result
    })


# ============================================================
# DOWNLOAD
# ============================================================
@app.route("/download", methods=["POST"])
def download_file():
    ipfs_hash = request.form.get("ipfs_hash")

    if not ipfs_hash:
        return jsonify({"error": "No IPFS hash provided"}), 400

    # Get filename from blockchain
    original_filename = None
    for block in blockchain.chain:
        if isinstance(block.data, dict):
            if block.data.get("ipfs_hash") == ipfs_hash:
                original_filename = block.data.get("file_name")

    if not original_filename:
        return jsonify({"error": "IPFS hash not found"}), 404

    # Download from IPFS
    try:
        temp_path = ipfs_client.download_file(ipfs_hash, DOWNLOAD_FOLDER)
    except Exception as e:
        return jsonify({"error": f"IPFS download failed: {str(e)}"}), 500

    final_path = os.path.join(DOWNLOAD_FOLDER, original_filename)
    os.rename(temp_path, final_path)

    return send_file(final_path, as_attachment=True)


# ============================================================
# TIMEZONE API
# ============================================================
@app.route("/timezone-info", methods=["GET"])
def timezone_info():
    region = request.args.get("region")
    return jsonify(get_timezone_info(region))


# ============================================================
# TRANSLATION API
# ============================================================
@app.route("/translate-ui", methods=["GET"])
def translate_ui():
    text = request.args.get("text", "Hello")
    lang = request.args.get("lang", "en")
    return jsonify(translate(text, lang))


# ============================================================
# Run App
# ============================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
