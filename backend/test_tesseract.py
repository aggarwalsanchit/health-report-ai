import pytesseract

# Optional: Specify the path if Tesseract is not detected automatically
# Uncomment and update the path if needed (Windows example)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("Tesseract Version:", pytesseract.get_tesseract_version())
