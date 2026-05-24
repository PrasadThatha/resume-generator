import pdfplumber
from docx import Document


def extract_text(file_path):

    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx(file_path)

    else:
        raise Exception("Unsupported File Format")


def extract_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    return text


def extract_docx(file_path):

    doc = Document(file_path)

    text = "\n".join([para.text for para in doc.paragraphs])

    return text