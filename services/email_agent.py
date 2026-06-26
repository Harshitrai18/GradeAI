from services.email_sender import send_email


def email_agent(student, pdf_path):

    status = send_email(
        student["Email"],
        pdf_path
    )

    return status