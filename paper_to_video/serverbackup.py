# server.py - FIXED TIMEOUT

from flask import Flask, request, jsonify, send_file, render_template_string
from pathlib import Path
import uuid
import threading
import subprocess
import os

app = Flask(__name__)

UPLOAD_DIR = Path('uploads')
OUTPUT_DIR = Path('output')
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

jobs = {}

HTML = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Paper to Video</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: monospace; 
            padding: 20px; 
            max-width: 800px; 
            margin: 0 auto;
            background: #fff;
            color: #000;
        }
        h1 { margin-bottom: 20px; border-bottom: 2px solid #000; padding-bottom: 10px; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #000; }
        input[type="file"] { display: block; margin: 10px 0; }
        button { 
            background: #000; 
            color: #fff; 
            border: none; 
            padding: 10px 20px; 
            cursor: pointer;
            font-family: monospace;
            font-size: 14px;
        }
        button:hover { background: #333; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        #status { 
            margin: 20px 0; 
            padding: 10px; 
            border: 1px solid #000; 
            min-height: 100px;
            font-size: 12px;
            white-space: pre-wrap;
        }
        .video-link { 
            display: block; 
            margin: 5px 0; 
            color: #00f;
            text-decoration: underline;
        }
        .error { color: #f00; }
        .success { color: #0a0; }
    </style>
</head>
<body>
    <h1>Paper to Video Generator</h1>
    
    <div class="section">
        <h2>1. Upload PDF</h2>
        <input type="file" id="pdfFile" accept=".pdf">
        <button id="uploadBtn" onclick="upload()">Generate Videos</button>
    </div>
    
    <div class="section">
        <h2>2. Status</h2>
        <div id="status">Ready. Upload a PDF to start.</div>
    </div>
    
    <div class="section">
        <h2>3. Generated Videos</h2>
        <div id="videos">No videos yet.</div>
    </div>

    <script>
        let statusDiv = document.getElementById('status');
        let videosDiv = document.getElementById('videos');
        let uploadBtn = document.getElementById('uploadBtn');

        function log(msg, type = 'info') {
            let timestamp = new Date().toLocaleTimeString();
            let color = type === 'error' ? 'error' : type === 'success' ? 'success' : '';
            statusDiv.innerHTML += `[${timestamp}] <span class="${color}">${msg}</span>\\n`;
            statusDiv.scrollTop = statusDiv.scrollHeight;
        }

        async function upload() {
            let file = document.getElementById('pdfFile').files[0];
            if (!file) {
                log('No file selected', 'error');
                return;
            }

            uploadBtn.disabled = true;
            statusDiv.innerHTML = '';
            videosDiv.innerHTML = 'Generating...';

            log('Uploading ' + file.name + '...');

            let formData = new FormData();
            formData.append('pdf', file);

            try {
                let response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Upload failed: ' + response.status);
                }

                let result = await response.json();
                log('Upload successful. Job ID: ' + result.job_id, 'success');
                
                pollStatus(result.job_id);

            } catch (error) {
                log('Error: ' + error.message, 'error');
                uploadBtn.disabled = false;
            }
        }

        async function pollStatus(jobId) {
            let interval = setInterval(async () => {
                try {
                    let response = await fetch('/status/' + jobId);
                    let data = await response.json();

                    log(data.message);

                    if (data.status === 'complete') {
                        clearInterval(interval);
                        log('Generation complete!', 'success');
                        showVideos(data.videos);
                        uploadBtn.disabled = false;
                    } else if (data.status === 'error') {
                        clearInterval(interval);
                        log('Error: ' + data.error, 'error');
                        uploadBtn.disabled = false;
                    }

                } catch (error) {
                    log('Polling error: ' + error.message, 'error');
                }
            }, 2000);
        }

        function showVideos(videos) {
            if (videos.length === 0) {
                videosDiv.innerHTML = 'No videos generated.';
                return;
            }

            let html = '<ul>';
            videos.forEach(v => {
                html += `<li><a href="/download/${v.file}" class="video-link">${v.title}</a> (${v.size})</li>`;
            });
            html += '</ul>';
            videosDiv.innerHTML = html;
        }
    </script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pdf']
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Not a PDF file'}), 400
    
    job_id = str(uuid.uuid4())[:8]
    pdf_path = UPLOAD_DIR / f"{job_id}.pdf"
    file.save(pdf_path)
    
    jobs[job_id] = {
        'status': 'processing',
        'message': 'Starting generation...',
        'videos': []
    }
    
    thread = threading.Thread(target=generate_videos, args=(job_id, pdf_path))
    thread.daemon = True  # Allow server to exit even if thread running
    thread.start()
    
    return jsonify({'job_id': job_id})

@app.route('/status/<job_id>')
def status(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(jobs[job_id])

@app.route('/download/<path:filename>')
def download(filename):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        return jsonify({'error': 'File not found'}), 404
    return send_file(file_path, as_attachment=True)

def generate_videos(job_id, pdf_path):
    """Background task - NO TIMEOUT"""
    try:
        jobs[job_id]['message'] = 'Running pipeline...'
        
        # Get absolute path to main.py
        project_root = Path(__file__).parent.parent
        main_py = project_root / 'main.py'
        
        print(f"[Job {job_id}] Running: python {main_py} {pdf_path}")
        
        # Run main.py with NO TIMEOUT
        result = subprocess.run(
            ['python', str(main_py), str(pdf_path.absolute())],
            capture_output=True,
            text=True,
            timeout=None,  # ← NO TIMEOUT! Let it run
            cwd=project_root
        )
        
        if result.returncode != 0:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error'] = result.stderr[-1000:]  # Last 1000 chars
            print(f"[Job {job_id}] ERROR:\n{result.stderr}")
            return
        
        print(f"[Job {job_id}] Success! Output:\n{result.stdout}")
        
        # Find generated videos
        output_name = pdf_path.stem
        output_path = project_root / 'output' / output_name
        
        if not output_path.exists():
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error'] = f'Output directory not found: {output_path}'
            return
        
        jobs[job_id]['message'] = 'Rendering videos...'
        
        videos = []
        for py_file in output_path.glob('video*.py'):
            video_num = py_file.stem  # e.g., 'video1'
            class_name = f'Video{video_num[5:]}'  # e.g., 'Video1'
            
            jobs[job_id]['message'] = f'Rendering {video_num}...'
            print(f"[Job {job_id}] Rendering {py_file} / {class_name}")
            
            render_result = subprocess.run(
                ['python', '-m', 'manim', '-ql', '--format=mp4', 
                 str(py_file), class_name],
                cwd=output_path,
                capture_output=True,
                text=True,
                timeout=None  # ← NO TIMEOUT on rendering either
            )
            
            if render_result.returncode == 0:
                # Find the rendered video
                video_path = output_path / 'media' / 'videos' / video_num / '480p15' / f'{class_name}.mp4'
                
                if video_path.exists():
                    import shutil
                    dest = OUTPUT_DIR / f'{job_id}_{video_num}.mp4'
                    shutil.copy(video_path, dest)
                    
                    videos.append({
                        'title': f'{class_name}.mp4',
                        'file': dest.name,
                        'size': f'{dest.stat().st_size // (1024*1024):.1f}MB'
                    })
                    print(f"[Job {job_id}] ✓ Saved {dest.name}")
                else:
                    print(f"[Job {job_id}] ⚠️  Video not found: {video_path}")
            else:
                print(f"[Job {job_id}] ⚠️  Render failed:\n{render_result.stderr}")
        
        jobs[job_id]['status'] = 'complete'
        jobs[job_id]['message'] = f'Generated {len(videos)} videos'
        jobs[job_id]['videos'] = videos
        
        print(f"[Job {job_id}] ✅ Complete! {len(videos)} videos")
        
    except Exception as e:
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = str(e)
        print(f"[Job {job_id}] ❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Paper to Video Server")
    print("="*60)
    print("\n  Open: http://localhost:8000")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, port=8000, host='0.0.0.0')