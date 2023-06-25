import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Loader from './Loader';
function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [predictedClass, setPredictedClass] = useState('');
  const [outputVideoPath, setOutputVideoPath] = useState('');
  const [loader,setLoader] = useState(false);
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
      setLoader(true);
      const response = await axios.post('http://localhost:5000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const { predicted_class, output_video } = response.data;
      console.log(response.data)
      setPredictedClass(predicted_class);
      setOutputVideoPath(output_video);
      setLoader(false);
    } catch (error) {
      console.error(error);
      alert('An error occurred during the prediction.');
      setLoader(false);
    }
  };

  return (
    <div className="container mx-auto flex justify-center items-center flex-col">
      <h1>Video Prediction</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".mp4, .avi" onChange={handleFileChange} />
        <button type="submit" className="border hover:text-white bg-red-200 px-10 py-2 mt-10">Submit</button>
      </form>

      {loader && <Loader/>}

      {  predictedClass &&  (
        <div>
          <h2 className="font-bold text-red-400 mt-10">Predicted Class: {predictedClass}</h2>
          {outputVideoPath && (
            <video src={require(`./assets/${outputVideoPath}`)} controls="controls" width="640" height="480" type="video/mp4" />
          )}
        </div>
      )}
    </div>
  );
}

export default App;
