from dotenv import load_dotenv
import os #The OS module in Python provides a way of using operating system dependent functionality
from email.message import EmailMessage #EmailMessage is a class that allows us to create an email message
import ssl #Add a layer of security to the email
import smtplib #Simple Mail Transfer Protocol (SMTP) is a protocol, which handles sending e-mail and routing e-mail between mail servers

load_dotenv()

email_sender = os.getenv('EMAIL_SENDER')
email_password = os.getenv('EMAIL_PASSWORD')
email_receiver = os.getenv('EMAIL_RECEIVER')

subject = 'Check out this cool website!'
body = 'This is the body of the email'

em = EmailMessage()

em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server: #Connect to the server using the SMTP_SSL class
    server.login(email_sender, email_password)
    server.send_message(em) #Send the email