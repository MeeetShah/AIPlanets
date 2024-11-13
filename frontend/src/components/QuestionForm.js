import React, { useState, useEffect } from "react";
import axios from "axios";

const QuestionForm = () => {
  const [pdfs, setPdfs] = useState([]);
  const [selectedPdf, setSelectedPdf] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    // Fetch the list of PDFs when the component mounts
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

  const handleQuestionSubmit = async (e) => {
    e.preventDefault();

    if (!selectedPdf || !question) {
      setErrorMessage("Please select a PDF and enter a question.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/ask-question/", {
        pdf_name: selectedPdf,
        question: question,
      });

      setAnswer(response.data.answer);
      setErrorMessage(""); // Clear any previous error message
    } catch (error) {
      setErrorMessage("Error asking question.");
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Ask a Question</h2>

      {/* Error message */}
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}

      <form onSubmit={handleQuestionSubmit}>
        {/* Select PDF */}
        <div>
          <label htmlFor="pdf-select">Select a PDF:</label>
          <select
            id="pdf-select"
            value={selectedPdf}
            onChange={(e) => setSelectedPdf(e.target.value)}
          >
            <option value="">Select PDF</option>
            {pdfs.map((pdf, index) => (
              <option key={index} value={pdf}>
                {pdf}
              </option>
            ))}
          </select>
        </div>

        {/* Question input */}
        <div>
          <label htmlFor="question-input">Your Question:</label>
          <input
            type="text"
            id="question-input"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
        </div>

        <button type="submit">Ask Question</button>
      </form>

      {/* Display answer */}
      {answer && (
        <div>
          <h3>Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default QuestionForm;
