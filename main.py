from fastapi import FastAPI, UploadFile, File, HTTPException
import pymupdf

app = FastAPI()

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        pdf_data = await file.read()
        doc = pymupdf.open(stream=pdf_data, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return {"filename": file.filename, "content": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
