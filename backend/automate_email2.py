from dotenv import load_dotenv
import os
from email.message import EmailMessage
import smtplib
import ssl
from jinja2 import Template  # For email templating
import schedule  # For scheduling emails
import time
import logging

load_dotenv()

# SMTP configuration
email_sender = os.getenv('EMAIL_SENDER')
email_password = os.getenv('EMAIL_PASSWORD')
smtp_server = 'smtp.gmail.com'
smtp_port = 465

# List of recipients
recipients = [
    'recipient1@example.com',
    'recipient2@example.com',
    'recipient3@example.com'
]

# Setup logger for error handling
logging.basicConfig(filename='email_log.log', level=logging.INFO)

# Sample CVE data
cve_details = {
    'title': 'CVE-2023-XXXX',
    'description': 'A critical vulnerability found in the system that allows remote code execution.',
    'mitigation': 'Apply the latest security patch to mitigate this vulnerability.'
}

# Email subject and HTML body using Jinja2 template
subject = 'New Critical Vulnerability Alert: {{ title }}'
html_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        h2 { color: #333; }
        p { font-size: 14px; }
    </style>
</head>
<body>
    <h2>{{ title }}</h2>
    <p>{{ description }}</p>
    <p><strong>Mitigation Strategies:</strong> {{ mitigation }}</p>
</body>
</html>
"""

def send_email(recipients, subject, html_content, attachments=None):
    context = ssl.create_default_context()

    for recipient in recipients:
        try:
            # Create EmailMessage
            msg = EmailMessage()
            msg['From'] = email_sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.set_content("This is a plain text alternative.")  # Plain text for fallback
            msg.add_alternative(html_content, subtype='html')  # HTML version

            # Add attachments if any
            if attachments:
                for attachment in attachments:
                    with open(attachment, 'rb') as f:
                        file_data = f.read()
                        file_name = os.path.basename(attachment)
                        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

            # Send the email
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(email_sender, email_password)
                server.send_message(msg)
            logging.info(f"Email sent successfully to {recipient}")

        except Exception as e:
            logging.error(f"Failed to send email to {recipient}: {e}")

# Function to render the email content with Jinja2 template
def render_email(cve_details):
    template = Template(html_template)
    return template.render(
        title=cve_details['title'],
        description=cve_details['description'],
        mitigation=cve_details['mitigation']
    )

# Function to check for new CVEs and send email if new ones are detected
def check_and_send_emails():
    # Logic to check for new CVEs goes here
    new_cve_detected = True  # Placeholder for real CVE detection logic

    if new_cve_detected:
        email_body = render_email(cve_details)
        email_subject = Template(subject).render(title=cve_details['title'])
        send_email(recipients, email_subject, email_body)

# Schedule the email to be sent daily
schedule.every().day.at("09:00").do(check_and_send_emails)

# Main loop to keep the scheduler running
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
