import requests
video_file_path = 'mixkit-married-couple-violently-arguing-4522-medium.mp4'

files = {'file': open(video_file_path, 'rb')}
response = requests.post('http://127.0.0.1:5000/predict', files=files)

data = response.json()

if 'error' in data:
    print('Error:', data['error'])
else:
    predicted_class = data['predicted_class']
    output_video_path = data['output_video']

    print('Predicted class:', predicted_class)
    print('Output video:', output_video_path)
