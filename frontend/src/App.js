import React, { useState } from 'react';
import axios from 'axios';
import './App.css';



function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [predictedClass, setPredictedClass] = useState('');
  const [outputVideoPath, setOutputVideoPath] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      alert('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const { predicted_class, output_video } = response.data;
      console.log(response.data)
      setPredictedClass(predicted_class);
      setOutputVideoPath(output_video);
    } catch (error) {
      console.error(error);
      alert('An error occurred during the prediction.');
    }
  };

  return (
    <div>
      <h1>Video Prediction</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".mp4, .avi" onChange={handleFileChange} />
        <button type="submit">Submit</button>
      </form>
      {predictedClass && (
        <div>
          <h2>Predicted Class: {predictedClass}</h2>
          {outputVideoPath && (
            <video src={outputVideoPath} controls="controls" width="640" height="480" type="video/mp4" />
          )}
        </div>
      )}
    </div>
  );
}

export default App;
