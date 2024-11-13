import React, { useState, useEffect } from "react";
import axios from "axios";

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
    <div>
      <h2>Uploaded PDFs</h2>
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      {pdfs.length > 0 ? (
        <ul>
          {pdfs.map((pdf, index) => (
            <li key={index}>{pdf}</li>
          ))}
        </ul>
      ) : (
        <p>No PDFs uploaded yet.</p>
      )}
    </div>
  );
};

export default PdfList;
