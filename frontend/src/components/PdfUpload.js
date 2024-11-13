import React, { useState } from "react";
import axios from "axios";

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
    <div>
      <h2>Upload PDF</h2>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Upload</button>
      {uploadStatus && <p>{uploadStatus}</p>}
    </div>
  );
};

export default PdfUpload;
