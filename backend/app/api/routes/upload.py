# app/api/routes/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.concurrency import run_in_threadpool
import os
import uuid
from app.services.ocr_service import (
    extract_text_from_pdf,
    extract_text_from_image,
)
from app.services.ai_service import analyze_report
from app.utils.file_validation import validate_file
from app.core.logging import logger

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", status_code=status.HTTP_200_OK)
async def upload_report(file: UploadFile = File(...)):
    try:
        validate_file(file)

        file_id = str(uuid.uuid4())
        extension = file.filename.split(".")[-1].lower()
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{extension}")

        # Save file efficiently
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Run OCR in threadpool for performance
        if extension == "pdf":
            text = await run_in_threadpool(extract_text_from_pdf, file_path)
        else:
            text = await run_in_threadpool(extract_text_from_image, file_path)

        # AI Analysis
        analysis = await run_in_threadpool(analyze_report, text)

        # 50% preview for non-logged-in users
        preview = analysis["analysis"][: len(analysis["analysis"]) // 2]

        return {
            "success": True,
            "file_id": file_id,
            "preview": preview,
            "message": "Login to view full analysis",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Upload processing failed")
        raise HTTPException(
            status_code=500,
            detail="Failed to process the uploaded report.",
        )
