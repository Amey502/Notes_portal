
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import torch
import re


pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\TesseractOCR\\tesseract.exe"


MODEL_NAME = "facebook/bart-large-cnn"

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)


def preprocess_text(text):
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    
    text = " ".join(text.split())

    
    text = re.sub(r'[^a-zA-Z0-9.,!?()\- ]+', ' ', text)

    return text


def split_into_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)


def chunk_text_by_sentences(text, max_words=350):
    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = []
    word_count = 0

    for sentence in sentences:
        words = sentence.split()

        if word_count + len(words) > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            word_count = 0

        current_chunk.append(sentence)
        word_count += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def summarize_chunk(chunk):
    inputs = tokenizer(
        chunk,
        max_length=1024,
        truncation=True,
        return_tensors="pt"
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        summary_ids = model.generate(
        inputs["input_ids"],
        max_length=250,
        min_length=80,
        num_beams=4,
        repetition_penalty=1.3,
        length_penalty=0.8,
        early_stopping=True
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


def summarize_text(text):
    text = preprocess_text(text)


    if len(text.split()) < 80:
        return text

    chunks = chunk_text_by_sentences(text)

    chunk_summaries = []
    for chunk in chunks:
        if chunk.strip():
            summary = summarize_chunk(chunk)
            chunk_summaries.append(summary)

    combined_summary = " ".join(chunk_summaries)

  
    final_summary = summarize_chunk(combined_summary)

    return final_summary


def extract_pdf_text(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print("PDF extraction error:", e)

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

        try:
            osd = pytesseract.image_to_osd(image)
            rotation = int(re.search(r'Rotate: (\d+)', osd).group(1))
            if rotation != 0:
                image = image.rotate(-rotation, expand=True)
        except:
            pass  

       
        text += pytesseract.image_to_string(image, config='--psm 6')

    return text


def get_combined_text(content, pdf_path=None):
    pdf_text = ""

    if pdf_path:
        if is_scanned_pdf(pdf_path):
            pdf_text = extract_text_with_ocr(pdf_path)
        else:
            pdf_text = extract_pdf_text(pdf_path)


    print("PDF TEXT LENGTH:", len(pdf_text))


    if pdf_text.strip():
        combined_text = pdf_text
    else:
        combined_text = content or ""

    combined_text = preprocess_text(combined_text)

    print("TEXT SAMPLE:", combined_text[:300])

    return combined_text