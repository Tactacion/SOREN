from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import subprocess
from pathlib import Path
import settings as config
from main import process_pdf

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = config.UPLOAD_DIR / filename
            file.save(str(filepath))
            
            # Process the PDF
            output_dir = process_pdf(filepath)
            
            # Generate the video using Manim
            video_file = output_dir / "video1.py"
            output_video = output_dir / "Video1.mp4"
            
            # Run Manim to create the video
            cmd = f"python -m manim -pql {video_file} Video1"
            subprocess.run(cmd, shell=True, cwd=str(output_dir))
            
            return jsonify({
                'success': True,
                'video_path': str(output_video),
                'message': 'Video generated successfully'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/video/<path:filename>')
def get_video(filename):
    video_path = config.OUTPUT_DIR / filename
    if video_path.exists():
        return send_file(str(video_path), mimetype='video/mp4')
    return jsonify({'error': 'Video not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)