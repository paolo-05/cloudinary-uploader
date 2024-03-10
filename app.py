import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import cloudinary
import cloudinary.api
import cloudinary.uploader

# Load environment variables from .env file
load_dotenv()

cloudinary.config(
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
  api_key = os.getenv("CLOUDINARY_API_KEY"),
  api_secret = os.getenv("CLOUDINARY_API_SECRET"),
  secure=True
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}


@app.route('/')
def hello():
    return 'Hello'

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if Authorization header is present
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer'):
        return jsonify({"error": "Unauthorized"}), 401
    
    # Extract token from Authorization header
    token = auth_header.split(' ')[1]

    # Here, you can validate the token, for example, using JWT or any other method
    ## NO ACTUAL VALIDATION.
    if token == '':
        return jsonify({"error": "Unauthorized"}), 401

    file_to_upload = request.files['file']
    if file_to_upload:
        # Upload file to Cloudinary
        result = cloudinary.uploader.upload(file_to_upload)
        return jsonify({"url": result['secure_url']})
    else:
        return jsonify({"error": "No file provided"}), 400
