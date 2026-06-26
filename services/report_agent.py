from services.pdf_generator import generate_pdf


def report_agent(student):

    pdf_path = generate_pdf(
        student,
        student["AI_Feedback"]
    )

    return pdf_path