from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from decouple import config

def send_mail(subject, body, reciever_email):
    message = MIMEMultipart()
    message["from"] = "PayAboki"
    message["to"] = reciever_email
    message["subject"] = subject
    message.attach(MIMEText(body))

    try:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(config('EMAIL_HOST_USER'), config('EMAIL_HOST_PASSWORD'))
            smtp.send_message(message)
            print("Done")
    except:
        pass
