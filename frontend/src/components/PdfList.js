import React, { useState, useEffect } from "react";
import axios from "axios";
import './UploadedPDFsStyles.css'; 
const PdfList = () => {
  const [pdfs, setPdfs] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    // Fetch the list of PDFs from the backend
    const fetchPdfs = async () => {
      try {
        const response = await axios.get("http://localhost:8000/pdfs/");
        setPdfs(response.data.pdfs);
      } catch (error) {
        setErrorMessage("Error fetching PDF list");
        console.error(error);
      }
    };

    fetchPdfs();
  }, []);

  return (
    <div className="uploaded-pdfs-container">
      <h2 className="uploaded-pdfs-heading">Uploaded PDFs</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      {pdfs.length > 0 ? (
        <ul className="pdf-list">
          {pdfs.map((pdf, index) => (
            <li key={index} className="pdf-item">{pdf}</li>
          ))}
        </ul>
      ) : (
        <p className="no-pdfs-message">No PDFs uploaded yet.</p>
      )}
    </div>
  );
};

export default PdfList;
