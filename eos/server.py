from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import traceback
from pathlib import Path
import json

# Import our custom modules
import settings as cfg
from main import process_pdf_to_video
from doubt_handler import DoubtHandler
from context_extractor import VideoContextExtractor

app = Flask(__name__)
CORS(app)  # Allow requests from your React frontend

# Configure a path to serve the final videos
VIDEO_DIR = cfg.OUTPUT_DIR
app.config['VIDEO_DIR'] = str(VIDEO_DIR)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Backend is running!'}), 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    print("\n" + "="*60)
    print("  [SERVER] /api/upload request received")
    print("="*60)
        
    if 'file' not in request.files:
        print("  [SERVER] Error: No 'file' part in request.")
        return jsonify({'success': False, 'error': 'No file part in request'}), 400
            
    file = request.files['file']
    if file.filename == '':
        print("  [SERVER] Error: No file selected.")
        return jsonify({'success': False, 'error': 'No selected file'}), 400
            
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = cfg.UPLOAD_DIR / filename
        
        try:
            # 1. Save the uploaded file
            print(f"  [SERVER] Saving file to: {filepath}")
            file.save(str(filepath))
            
            # 2. Run the A-P-G pipeline (Analyze, Plan, Generate)
            print(f"  [SERVER] Starting A-P-G pipeline for {filename}...")
            script_path, scene_name = process_pdf_to_video(filepath)
            
            # 3. Render directly - code is PERFECT from Zero-Error Generator!
            print(f"  [SERVER] Rendering perfect code (no supervisor needed!)...")
            import subprocess
            result = subprocess.run(
                ["python3", "-m", "manim", "render", "-ql", str(script_path), scene_name],
                capture_output=True,
                text=True,
                cwd=str(script_path.parent)
            )

            if result.returncode != 0:
                # This should NEVER happen with Zero-Error Generator!
                print("  [SERVER] ⚠️ Unexpected render failure!")
                print(result.stderr)
                raise Exception("Render failed - Zero-Error Generator guarantee broken!")
            
            # 4. Find the final video file
            video_output_path = script_path.parent / "media" / "videos" / scene_name / "480p15" / f"{scene_name}.mp4"
            
            if not video_output_path.exists():
                print(f"  [SERVER] Error: Render finished but MP4 file not found at {video_output_path}")
                return jsonify({'success': False, 'error': 'Render finished but final MP4 not found.'}), 500
            
            # 5. Create a URL path for the frontend to fetch the video
            # This path is relative to the VIDEO_DIR
            relative_video_path = video_output_path.relative_to(VIDEO_DIR)
            
            print(f"  [SERVER] ✅ Success! Video URL: /api/video/{relative_video_path}")
            return jsonify({
                'success': True,
                'video_path': f'/api/video/{relative_video_path.as_posix()}',
                'video_id': script_path.parent.name,
                'message': 'Video generated successfully'
            }), 200

        except Exception as e:
            print(f"  [SERVER] 🚨 Unhandled Exception in /api/upload:")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'An internal server error occurred: {str(e)}'
            }), 500
    else:
        print(f"  [SERVER] Error: Invalid file type. Only PDFs are allowed.")
        return jsonify({'success': False, 'error': 'Invalid file type. Only PDFs are allowed.'}), 400

@app.route('/api/video/<path:filename>')
def get_video(filename):
    """Serves the generated video files."""
    print(f"  [SERVER] /api/video request for: {filename}")
    try:
        return send_from_directory(
            app.config['VIDEO_DIR'],
            filename,
            as_attachment=False
        )
    except FileNotFoundError:
        print(f"  [SERVER] Error: Video file not found.")
        return jsonify({'success': False, 'error': 'File not found'}), 404


@app.route('/api/output/<path:filepath>')
def serve_output_file(filepath):
    """Serve files from output directory (videos, pdfs, etc.)"""
    print(f"  [SERVER] /api/output request for: {filepath}")
    try:
        output_dir = Path(__file__).parent / 'output'
        return send_from_directory(
            output_dir,
            filepath,
            as_attachment=False
        )
    except FileNotFoundError:
        print(f"  [SERVER] Error: Output file not found: {filepath}")
        return jsonify({'success': False, 'error': 'File not found'}), 404


@app.route('/api/demo/demo.mp4')
def get_demo_video():
    """Serves the demo.mp4 from the root eos directory."""
    print(f"  [SERVER] /api/demo/demo.mp4 request received")
    try:
        # Get the eos root directory (parent of backend)
        eos_root = Path(__file__).parent.parent
        return send_from_directory(
            eos_root,
            'demo.mp4',
            as_attachment=False
        )
    except FileNotFoundError:
        print(f"  [SERVER] Error: Demo video file not found.")
        return jsonify({'success': False, 'error': 'Demo video not found'}), 404


@app.route('/api/demo/context', methods=['POST'])
def get_demo_context():
    """Get context from gag.pdf and gag/video1.py for Q&A"""
    print(f"  [SERVER] /api/demo/context request received")
    try:
        data = request.json
        question = data.get('question', '')

        # Read gag.pdf
        pdf_path = Path(__file__).parent / 'gag.pdf'
        manim_code_path = Path(__file__).parent / 'output' / 'gag' / 'video1.py'

        context = {
            'pdf_available': pdf_path.exists(),
            'manim_code_available': manim_code_path.exists()
        }

        # Read Manim code for context
        if manim_code_path.exists():
            with open(manim_code_path, 'r') as f:
                context['manim_code'] = f.read()

        # Read PDF text
        if pdf_path.exists():
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    pdf_text = ''
                    for page in pdf_reader.pages[:10]:  # First 10 pages
                        pdf_text += page.extract_text()
                    context['pdf_text'] = pdf_text[:5000]  # Limit to 5000 chars
            except Exception as e:
                print(f"  [SERVER] Error reading PDF: {e}")
                context['pdf_text'] = ''

        return jsonify({'success': True, 'context': context}), 200
    except Exception as e:
        print(f"  [SERVER] Error getting context: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/context', methods=['POST'])
def get_context():
    """Get PDF and Manim code context for Q&A based on video mapping"""
    print(f"  [SERVER] /api/context request received")
    try:
        data = request.json
        question = data.get('question', '')
        pdf_name = data.get('pdf_name', 'gag.pdf')
        output_folder = data.get('output_folder', 'gag')
        video_id = data.get('video_id', 'video1')

        print(f"  [SERVER] Context request for PDF: {pdf_name}, Output: {output_folder}")

        # Read the PDF
        pdf_path = Path(__file__).parent / pdf_name
        if not pdf_path.exists():
            # Try uploads directory
            pdf_path = cfg.UPLOAD_DIR / pdf_name
        
        # Read Manim code
        manim_code_path = Path(__file__).parent / 'output' / output_folder / 'video1.py'

        context = {
            'pdf_available': pdf_path.exists(),
            'manim_code_available': manim_code_path.exists(),
            'pdf_name': pdf_name,
            'output_folder': output_folder
        }

        # Read Manim code for context
        if manim_code_path.exists():
            with open(manim_code_path, 'r') as f:
                context['manim_code'] = f.read()
                print(f"  [SERVER] ✅ Loaded Manim code from {manim_code_path}")
        else:
            print(f"  [SERVER] ⚠️ Manim code not found at {manim_code_path}")
            context['manim_code'] = ''

        # Read PDF text
        if pdf_path.exists():
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    pdf_text = ''
                    for page in pdf_reader.pages[:10]:  # First 10 pages
                        pdf_text += page.extract_text()
                    context['pdf_text'] = pdf_text[:5000]  # Limit to 5000 chars
                    print(f"  [SERVER] ✅ Loaded PDF text from {pdf_path}")
            except Exception as e:
                print(f"  [SERVER] ⚠️ Error reading PDF: {e}")
                context['pdf_text'] = ''
        else:
            print(f"  [SERVER] ⚠️ PDF not found at {pdf_path}")
            context['pdf_text'] = ''

        return jsonify({'success': True, 'context': context}), 200
    except Exception as e:
        print(f"  [SERVER] 🚨 Error getting context: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/videos/list', methods=['GET'])
def list_videos():
    """List all available rendered videos."""
    print("  [SERVER] /api/videos/list request received")

    try:
        videos = []
        output_dir = Path(cfg.OUTPUT_DIR)

        # Add demo video first
        demo_video_path = Path(__file__).parent.parent / 'demo.mp4'
        if demo_video_path.exists():
            videos.append({
                'id': 'demo_video1',
                'path': '/api/demo/demo.mp4',
                'title': 'Demo: Multi-Marginal Schrödinger Bridges',
                'description': 'A demonstration video explaining multi-marginal Schrödinger bridges and optimal transport.',
                'thumbnail': '/api/demo/demo.mp4',
                'is_demo': True
            })

        # Find all video files
        for project_dir in output_dir.iterdir():
            if not project_dir.is_dir():
                continue

            # Look for video files in media/videos
            media_videos = project_dir / "media" / "videos"
            if media_videos.exists():
                for video_file in media_videos.rglob("*.mp4"):
                    # Skip partial files
                    if 'partial' in str(video_file):
                        continue

                    # Get relative path
                    rel_path = video_file.relative_to(cfg.OUTPUT_DIR)

                    # Try to load metadata
                    metadata = {
                        'id': project_dir.name,
                        'path': f'/api/video/{rel_path.as_posix()}',
                        'title': project_dir.name,
                        'thumbnail': f'/api/video/{rel_path.as_posix()}',
                        'is_demo': False
                    }

                    # Try to load analysis for better metadata
                    analysis_files = list(project_dir.glob('*_analysis.json'))
                    if analysis_files:
                        with open(analysis_files[0], 'r') as f:
                            analysis = json.load(f)
                            metadata['title'] = analysis.get('title', project_dir.name)
                            metadata['description'] = analysis.get('summary', '')

                    videos.append(metadata)

        print(f"  [SERVER] Found {len(videos)} videos")
        return jsonify({'success': True, 'videos': videos}), 200

    except Exception as e:
        print(f"  [SERVER] Error listing videos: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/videos/<video_id>/metadata', methods=['GET'])
def get_video_metadata(video_id):
    """Get metadata for a specific video."""
    print(f"  [SERVER] /api/videos/{video_id}/metadata request received")

    try:
        # Special case for demo video
        if video_id == 'demo_video1':
            project_dir = Path(cfg.OUTPUT_DIR) / 'gag'
            metadata = {
                'id': 'demo_video1',
                'title': 'Demo: Multi-Marginal Schrödinger Bridges',
                'description': 'A demonstration video explaining multi-marginal Schrödinger bridges and optimal transport.',
                'path': '/api/demo/demo.mp4',
                'key_concepts': [
                    'Schrödinger Bridges',
                    'Optimal Transport',
                    'Multi-Marginal Problems',
                    'Entropy Regularization'
                ],
                'is_demo': True
            }

            # Try to load demo analysis if exists
            if project_dir.exists():
                analysis_files = list(project_dir.glob('*_analysis.json'))
                if analysis_files:
                    with open(analysis_files[0], 'r') as f:
                        analysis = json.load(f)
                        metadata.update({
                            'key_concepts': analysis.get('key_concepts', metadata['key_concepts']),
                            'main_contributions': analysis.get('main_contributions', []),
                        })

            print(f"  [SERVER] Demo metadata loaded")
            return jsonify({'success': True, 'metadata': metadata}), 200

        # Regular video
        project_dir = Path(cfg.OUTPUT_DIR) / video_id

        if not project_dir.exists():
            return jsonify({'success': False, 'error': 'Video not found'}), 404

        metadata = {
            'id': video_id,
            'title': video_id,
            'is_demo': False
        }

        # Load analysis
        analysis_files = list(project_dir.glob('*_analysis.json'))
        if analysis_files:
            with open(analysis_files[0], 'r') as f:
                analysis = json.load(f)
                metadata.update({
                    'title': analysis.get('title', video_id),
                    'description': analysis.get('summary', ''),
                    'key_concepts': analysis.get('key_concepts', []),
                    'main_contributions': analysis.get('main_contributions', []),
                })

        # Load scripts
        script_files = list(project_dir.glob('*_scripts.json'))
        if script_files:
            with open(script_files[0], 'r') as f:
                scripts = json.load(f)
                metadata['scripts'] = scripts

        print(f"  [SERVER] Metadata loaded for {video_id}")
        return jsonify({'success': True, 'metadata': metadata}), 200

    except Exception as e:
        print(f"  [SERVER] Error loading metadata: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/doubt', methods=['POST'])
def ask_doubt():
    """Handle student doubt/question about video content."""
    print("  [SERVER] /api/doubt request received")

    try:
        data = request.json
        question = data.get('question')
        video_id = data.get('video_id')
        timestamp = data.get('timestamp', 0.0)

        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400

        if not video_id:
            return jsonify({'success': False, 'error': 'No video_id provided'}), 400

        print(f"  [SERVER] Question: {question}")
        print(f"  [SERVER] Video ID: {video_id}")
        print(f"  [SERVER] Timestamp: {timestamp}s")

        # Get extra context if provided (PDF + Manim code)
        extra_context = data.get('extra_context', {})
        pdf_name = extra_context.get('pdf_name', 'gag.pdf')
        output_folder = extra_context.get('output_folder', 'gag')
        
        print(f"  [SERVER] Using context: PDF={pdf_name}, Output={output_folder}")

        # Find the project directory based on output folder
        project_dir = Path(cfg.OUTPUT_DIR) / output_folder

        if not project_dir.exists():
            print(f"  [SERVER] ⚠️ Project directory not found: {project_dir}")
            # Fallback to video_id
            project_dir = Path(cfg.OUTPUT_DIR) / video_id.replace('video1_', '').replace('video2_', '')
            if not project_dir.exists():
                # Try just the first part before underscore
                fallback = video_id.split('_')[0] if '_' in video_id else video_id
                project_dir = Path(cfg.OUTPUT_DIR) / fallback
                if not project_dir.exists():
                    return jsonify({'success': False, 'error': 'Video project not found'}), 404

        print(f"  [SERVER] Using project directory: {project_dir}")

        # Find video path
        video_path = None

        # Special case for demo video
        if 'demo' in video_id.lower():
            demo_video_path = Path(__file__).parent.parent / 'demo.mp4'
            if demo_video_path.exists():
                video_path = demo_video_path
        else:
            # Regular video path for generated videos
            media_videos = project_dir / "media" / "videos"
            if media_videos.exists():
                for video_file in media_videos.rglob("*.mp4"):
                    if 'partial' not in str(video_file):
                        video_path = video_file
                        print(f"  [SERVER] Found video: {video_path}")
                        break

        # Extract context
        extractor = VideoContextExtractor(
            project_dir=str(project_dir),
            video_path=str(video_path) if video_path else None
        )
        context = extractor.extract_context(timestamp=timestamp)

        # Add extra context from the request (PDF + Manim code)
        if extra_context:
            context['extra_pdf_text'] = extra_context.get('pdf_text', '')
            context['extra_manim_code'] = extra_context.get('manim_code', '')
            context['source_pdf'] = pdf_name
            context['output_folder'] = output_folder
            print(f"  [SERVER] Added extra context from {pdf_name}")

        # Get answer from doubt handler
        handler = DoubtHandler()
        result = handler.answer_question(
            question=question,
            context=context,
            style="educational"
        )

        print(f"  [SERVER] ✅ Answer generated ({len(result['answer'])} chars)")
        return jsonify({
            'success': True,
            'answer': result['answer'],
            'sources': result['sources'],
            'context_used': result['context_used']
        }), 200

    except Exception as e:
        print(f"  [SERVER] 🚨 Error handling doubt: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🎬 Fullstack Manim Video Backend Server 🎬")
    print("="*60)
    print(f"  Mode: {'Debug' if os.environ.get('FLASK_DEBUG') else 'Production'}")
    print(f"  Listening on: http://127.0.0.1:5001")
    print(f"  Uploads will be saved to: {cfg.UPLOAD_DIR}")
    print(f"  Outputs will be saved to: {cfg.OUTPUT_DIR}")
    print("="*60 + "\n")
    app.run(debug=False, port=5001, host='127.0.0.1')