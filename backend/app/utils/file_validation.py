# app/utils/file_validation.py
from fastapi import UploadFile, HTTPException
from app.core.config import settings


def validate_file(file: UploadFile):
    extension = file.filename.split(".")[-1].lower()

    if extension not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF and images are allowed.",
        )

    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the allowed limit.",
        )
