import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = os.getenv("GMAIL_EMAIL")
EMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# Send an email
def send_email(email: str, subject: str, message: str):
    # Initialize the SMTP server
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.starttls()
    smtpserver.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    try:
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        smtpserver.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        print(f"Email sent to {email}")

    except Exception as e:
        print(f"Failed to send email to {email}. Error: {e}")

    finally:
        smtpserver.quit()