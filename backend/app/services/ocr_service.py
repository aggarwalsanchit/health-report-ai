# app/services/ocr_service.py
import fitz
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from app.core.logging import logger


def extract_text_from_pdf(file_path: str) -> str:
    try:
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()

        if len(text.strip()) < 50:
            images = convert_from_path(file_path)
            for img in images:
                text += pytesseract.image_to_string(img, lang="eng+hin+pan")

        if not text.strip():
            raise ValueError("No readable text found in the document.")

        return text

    except Exception as e:
        logger.exception("OCR processing failed")
        raise RuntimeError("Failed to extract text from the document.") from e


def extract_text_from_image(file_path: str) -> str:
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang="eng+hin+pan")

        if not text.strip():
            raise ValueError("No readable text found in the image.")

        return text

    except Exception as e:
        logger.exception("Image OCR failed")
        raise RuntimeError("Failed to extract text from the image.") from e
