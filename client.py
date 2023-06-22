import requests

# Specify the file path of the video you want to predict
video_file_path = 'mixkit-married-couple-violently-arguing-4522-medium.mp4'

# Create a POST request to the Flask server
files = {'file': open(video_file_path, 'rb')}
response = requests.post('http://127.0.0.1:5000/predict', files=files)

# Parse the response JSON
data = response.json()

# Check if the request was successful
if 'error' in data:
    print('Error:', data['error'])
else:
    # Get the predicted class and output video file path from the response
    predicted_class = data['predicted_class']
    output_video_path = data['output_video']

    print('Predicted class:', predicted_class)
    print('Output video:', output_video_path)
