import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from smolagents import CodeAgent, tool
import os

EMAIL_BASE = {'kseniia' : 'kseniia.strelbytska@gmail.com'}

@tool
def send_email(text: str, recipient: str) -> bool:
    """
    Sends an email to the recipient's email address.

    Args:
        text: The string containting email content.
        recipient: The string containing recipient email address OR recipient name if address is not given.
        
    Returns: 
        bool: True if submission was successful, False if errors occured.
    """

    if '@' not in recipient:
        recipient = recipient.lower()
        recipient = EMAIL_BASE[recipient]
    
    try:
        port = 587
        server = "smtp.gmail.com"

        email_sender = "INSERT EMAIL"
        email_recepient = recipient
        email_password = os.getenv("email_password")

        message = MIMEText(f"{text}", "html")
        message["Subject"] = "multipart test"
        message["From"] = email_sender
        message["To"] = email_recepient

        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", port) as server:
            server.starttls(context=context)
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_recepient, message.as_string())
        
        return True
    except:
        return False
