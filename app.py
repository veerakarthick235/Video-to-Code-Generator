from flask import Flask, render_template, request, jsonify
import time
import os
from video_processor import analyze_video_for_code 


app = Flask(__name__)


app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024 
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define allowed video file extensions
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Renders the main upload page."""
    return render_template('index.html')

@app.route('/generate-code', methods=['POST'])
def generate_code():
    """Handles video upload, saves it, and runs the analysis logic."""
    
    if 'videoFile' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['videoFile']
    
    if video_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(video_file.filename):
         return jsonify({'error': f'File type not supported. Use {", ".join(ALLOWED_EXTENSIONS)}.'}), 400

    filename = video_file.filename
    timestamp = str(int(time.time()))
    safe_filename = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    
    try:
        video_file.save(filepath)
    except Exception as e:
        return jsonify({'error': f'Could not save file (Limit is {app.config["MAX_CONTENT_LENGTH"] / (1024*1024)} MB): {e}'}), 500


    print(f"\nStarting analysis for video: {filepath}")
    
    generated_code = analyze_video_for_code(filepath)
    
    
 
    if generated_code:
        return jsonify({
            'success': True,
            'html': generated_code['html'],
            'css': generated_code['css'],
            'js': generated_code['js']
        })
    else:
        return jsonify({'error': 'Analysis failed to produce structured code.'}), 500

if __name__ == '__main__':
    print("\n--- Starting Flask Server ---")
    app.run(debug=True)