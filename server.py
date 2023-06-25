from keras.models import load_model
from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
from collections import deque
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'mp4'}
SEQUENCE_LENGTH = 16
IMAGE_HEIGHT = 64
IMAGE_WIDTH = 64
CLASSES_LIST = ['NonViolence', 'Violence'] 

MoBiLSTM_model = load_model('violence.h5')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_frames(video_file_path, output_file_path):
   
    video_reader = cv2.VideoCapture(video_file_path)
    original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video_writer = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                   video_reader.get(cv2.CAP_PROP_FPS), (original_video_width, original_video_height))

    frames_queue = deque(maxlen=SEQUENCE_LENGTH)

    predicted_class_name = ''
    violence_count = 0

    while video_reader.isOpened():
        ok, frame = video_reader.read()

        if not ok:
            break
        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        normalized_frame = resized_frame / 255
        frames_queue.append(normalized_frame)
        if len(frames_queue) == SEQUENCE_LENGTH:
            predicted_labels_probabilities = MoBiLSTM_model.predict(np.expand_dims(frames_queue, axis=0))[0]
            predicted_label = np.argmax(predicted_labels_probabilities)
            predicted_class_name = CLASSES_LIST[predicted_label]
            if predicted_class_name == "Violence":
                violence_count += 1
        if predicted_class_name == "Violence":
            cv2.putText(frame, predicted_class_name, (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 12)
        else:
            cv2.putText(frame, predicted_class_name, (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 12)
        video_writer.write(frame)

    video_reader.release()
    video_writer.release()
    predicted_class_name = "Violence" if violence_count > 0 else "NonViolence"

    return predicted_class_name

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    if file and allowed_file(file.filename):
        file_path = 'video_file.mp4'
        file.save(file_path)
        output_folder_path = os.path.join('frontend', 'src', 'assets')
        os.makedirs(output_folder_path, exist_ok=True)
        output_file_path = os.path.join(output_folder_path, 'output.mp4')
        predicted_class = predict_frames(file_path, output_file_path)
        return jsonify({'message': 'Prediction completed', 'predicted_class': predicted_class, 'output_video': output_file_path})

    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)
