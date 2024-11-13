import React, { useState } from "react";
import axios from "axios";
import './UploadStyles.css'; 

const PdfUpload = () => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!file) {
      setUploadStatus("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload-pdf/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setUploadStatus(response.data.message);
    } catch (error) {
      setUploadStatus("Error uploading file.");
      console.error(error);
    }
  };

  return (
    <div className="upload-container">
      <h1>PDF Upload and Question Answering</h1>
    <h2 className="upload-heading">Upload Your PDF</h2>
    <div className="file-input-container">
      <input 
        type="file" 
        accept="application/pdf" 
        onChange={handleFileChange} 
        className="file-input" 
      />
      <button 
        onClick={handleFileUpload} 
        className="upload-button"
      >
        Upload
      </button>
    </div>
    {uploadStatus && <p className="status-message">{uploadStatus}</p>}
  </div>
  );
};

export default PdfUpload;
