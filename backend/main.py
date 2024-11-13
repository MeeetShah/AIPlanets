from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

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
pdf_directory = "pdfs"  # Replace with your actual path for PDFs

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

@app.post("/ask-question/")
async def ask_question(request: QuestionRequest):
    pdf_name = request.pdf_name
    question = request.question

    # Check if the PDF exists
    if pdf_name not in get_uploaded_pdfs():
        raise HTTPException(status_code=404, detail="PDF not found")

    # Process the question (replace this with your actual NLP logic)
    answer = process_question(pdf_name, question)

    return {"answer": answer}
