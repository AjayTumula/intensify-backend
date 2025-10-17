from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.file_parser import parse_excel_or_csv, parse_pdf
import io, json

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    try:
        contents = await file.read()
        bio = io.BytesIO(contents)
        if filename.lower().endswith(('.xls', '.xlsx', '.csv')):
            docs = parse_excel_or_csv(bio, filename)
            # for LLM content sample a slice
            sampled = docs[:20]
            context_text = json.dumps(sampled, default=str)
            return {"status":"ok", "count":len(docs), "sample": sampled}
        elif filename.lower().endswith('.pdf'):
            lines = parse_pdf(bio)
            docs = [{"text": t} for t in lines]
            context_text = "\n".join(lines[:200])
            return {"status":"ok", "count":len(docs), "sample": docs[:10]}
        else:
            raise HTTPException(status_code=440, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
