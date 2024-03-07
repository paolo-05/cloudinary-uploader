from flask import request, jsonify
import cloudinary
from . import app

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if Authorization header is present
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401
    
    # Extract token from Authorization header
    token = auth_header.split(' ')[1]

    # Here, you can validate the token, for example, using JWT or any other method
    ## NO ACTUAL VALIDATION.
    if token is '':
        return jsonify({"error": "Unauthorized"}), 401

    file_to_upload = request.files['file']
    if file_to_upload:
        # Upload file to Cloudinary
        result = cloudinary.uploader.upload(file_to_upload)
        return jsonify({"public_id": result['public_id'], "url": result['secure_url']})
    else:
        return jsonify({"error": "No file provided"}), 400

