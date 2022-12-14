from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from decouple import config

message = MIMEMultipart()
message["from"] = "PayAboki Verification"
message["to"] = "najibkado@gmail.com"
message["subject"] = "This is a test"
message.attach(MIMEText("Body"))

with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(config('EMAIL_HOST_USER'), config('EMAIL_HOST_PASSWORD'))
    smtp.send_message(message)
    print("Done")
