from template import create_resume_pdf


# =========================================================
# GENERATE PDF
# =========================================================

def generate_pdf(resume_data):

    output_path = "UST_FORMATTED_RESUME.pdf"

    try:

        create_resume_pdf(

            resume_data,

            output_path

        )

        return output_path

    except Exception as error:

        print(

            f"PDF Generation Failed: {error}"

        )

        return None