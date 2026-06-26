import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_email(receiver_email, pdf_path):

    try:

        msg = EmailMessage()

        msg["Subject"] = "GradeAI Performance Report"
        msg["From"] = EMAIL
        msg["To"] = receiver_email

        msg.set_content(
            """
Hello,

Your latest GradeAI performance report is attached.

Regards,
GradeAI Team
"""
        )

        with open(pdf_path, "rb") as f:

            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_path)
            )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL,
                APP_PASSWORD
            )

            smtp.send_message(msg)

        return True

    except Exception as e:

        print(e)
        return False