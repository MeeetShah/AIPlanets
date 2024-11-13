from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI, UploadFile, Form
from langchain_openai import OpenAI
app = FastAPI()

# Set the upload directory
UPLOAD_DIRECTORY = "./uploads"

# Allow CORS from the React frontend (running on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure that the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Endpoint to upload PDF files
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Get the file path to save the file
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        
        # Save the file to the specified location
        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())
        
        return {"message": f"File '{file.filename}' uploaded successfully!"}
    
    except Exception as e:
        return JSONResponse(content={"message": f"Error uploading file: {str(e)}"}, status_code=500)

# Endpoint to get the list of uploaded PDFs
@app.get("/pdfs/")
async def get_uploaded_pdfs():
    try:
        # Get a list of PDF files in the upload directory
        pdf_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith('.pdf')]
        return {"pdfs": pdf_files}
    except Exception as e:
        return JSONResponse(content={"message": f"Error retrieving PDF list: {str(e)}"}, status_code=500)

from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

# Initialize the FastAPI app


# Define a request model to handle incoming question data
class QuestionRequest(BaseModel):
    pdf_name: str
    question: str

# Dummy storage for PDFs (replace with actual file storage if necessary)
pdf_directory = "uploads"  # Replace with your actual path for PDFs

# Example function to get a list of uploaded PDFs
def get_uploaded_pdfs():
    # This just returns the names of PDF files in the 'pdfs' directory
    if not os.path.exists(pdf_directory):
        return []
    return [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# Dummy NLP logic (replace with actual LangChain or LlamaIndex logic)
def process_question(pdf_name: str, question: str):
    # For now, just a basic check
    if question.lower() in pdf_name.lower():  # Simulating a simple match
        return f"Answer from {pdf_name}: The document contains information related to '{question}'."
    else:
        return "Sorry, I couldn't find an answer to your question."

@app.get("/pdf-list/")
async def get_pdf_list():
    # Return the list of uploaded PDFs
    return {"pdfs": get_uploaded_pdfs()}

# @app.post("/ask-question/")
# async def ask_question(pdf_name: str = Form(...), question: str = Form(...)):
#     pdf_path = f"uploads/{pdf_name}"
#     if not os.path.exists(pdf_path):
#         return {"error": "PDF file not found."}
    
#     # Call process_question to get the answer
#     answer = process_question(pdf_path, question)
    
#     return {"answer": answer}

# @app.post("/ask-question/")
# async def ask_question(request: QuestionRequest):
#     # Extract data from the request body
#     pdf_name = request.pdf_name
#     question = request.question

#     pdf_path = f"uploads/{pdf_name}"
#     if not os.path.exists(pdf_path):
#         return {"error": "PDF file not found."}
    
#     # Call process_question to get the answer
#     answer = process_question(pdf_path, question)
    
#     return {"answer": answer}
@app.post("/ask-question")
def ask_question(request: QuestionRequest):
    try:
        data = request.json()
        pdf = data.get("pdf")
        question = data.get("question")

        if not pdf or not question:
            raise HTTPException(status_code=400, detail="PDF and question are required")

        # Process the question and PDF, then return the answer
        answer = get_answer(pdf, question)

        return {"answer": answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import fitz  # PyMuPDF for PDF processing
from langchain.llms import OpenAI  # or appropriate LlamaIndex class

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file using PyMuPDF."""
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text += page.get_text("text")  # Extract text from each page
    return text

def process_question(pdf_path: str, question: str) -> str:
    """Extracts text from a PDF and answers the question using LangChain."""
    # Step 1: Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Initialize LangChain model
    llm = OpenAI()  # Or replace with LlamaIndex setup if preferred
    
    # Step 3: Pass the PDF text and question to the model
    response = llm({"text": pdf_text, "question": question})
    
    # Step 4: Return the answer
    return response["answer"]
