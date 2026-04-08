from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\TesseractOCR\\tesseract.exe"

MODEL_NAME = "facebook/bart-large-cnn"


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)



def clean_text(text):
    return " ".join(text.split())



def chunk_text(text, max_words=400):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]



def summarize_text(text):
    if not text:
        return ""

    chunks = chunk_text(text)
    final_summary = ""

    for chunk in chunks:
        inputs = tokenizer(
            chunk,
            max_length=1024,
            truncation=True,
            return_tensors="pt"
        )

        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=120,
            min_length=30,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True
        )

        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        final_summary += summary + " "

    return final_summary.strip()



def extract_pdf_text(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
    except:
        pass
    return text



def is_scanned_pdf(pdf_path, threshold=0.2):
    doc = fitz.open(pdf_path)
    text_pages = 0

    for page in doc:
        text = page.get_text().strip()
        if len(text) > 50:
            text_pages += 1

    ratio = text_pages / len(doc)
    return ratio < threshold



def extract_text_with_ocr(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))

        text += pytesseract.image_to_string(image)

    return text



def get_combined_text(content, pdf_path=None):
    combined_text = content or ""

    if pdf_path:
        if is_scanned_pdf(pdf_path):
            pdf_text = extract_text_with_ocr(pdf_path)
        else:
            pdf_text = extract_pdf_text(pdf_path)

        combined_text += " " + pdf_text

    return clean_text(combined_text)