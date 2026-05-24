import os

from extractor import extract_text
from parser import parse_resume
from pdf_generator import generate_pdf

INPUT_FOLDER = "input"


def process_resume():

    files = os.listdir(INPUT_FOLDER)

    if not files:
        print("No Resume Found")
        return

    file_name = files[0]

    input_path = os.path.join(INPUT_FOLDER, file_name)

    print("STEP 1 - Extracting Text")

    raw_text = extract_text(input_path)

    # print(raw_text)

    print("STEP 2 - Parsing Resume")

    parsed_data = parse_resume(raw_text)

    print("STEP 3 - Generating PDF")

    generated_pdf = generate_pdf(parsed_data)

    print(f"PDF Generated Successfully: {generated_pdf}")


if __name__ == "__main__":

    process_resume()