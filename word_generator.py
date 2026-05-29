from word_template import create_resume_docx


def generate_word(resume_data):

    output_path = "UST_FORMATTED_RESUME.docx"

    try:

        create_resume_docx(
            resume_data,
            output_path
        )

        return output_path

    except Exception as error:

        print(f"Word Generation Failed: {error}")

        return None