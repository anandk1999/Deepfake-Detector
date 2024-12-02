import os

from flask import Flask, request, jsonify, render_template
from utils import extract_frames, preprocess_frames
from model import DeepFakeDetector, load_model, predict
from absl import flags, app

# Flags
FLAGS = flags.FLAGS
flags.DEFINE_integer('num_frames', 40, 'Number of Frames to extract from video')

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the deep fake detector model
model = load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        result = analyze_video(filepath)
        return jsonify(result)

def analyze_video(video_path):
    frames = extract_frames(video_path, )
    processed_frames = preprocess_frames(frames)
    prediction, confidence = predict(model, processed_frames)
    return {
        "is_deepfake": prediction,
        "confidence": confidence
    }

if __name__ == '__main__':
    app.run(debug=True)