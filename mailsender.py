from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication  # Import MIMEApplication for PDF attachment
from email.mime.image import MIMEImage  # Import MIMEImage for image attachment
from email.mime.text import MIMEText
import smtplib
import logging

# Function to read sender's password from a text file
def read_sender_password():
    with open("password.txt", "r") as file:
        return file.read().strip()

# Configure logging
logging.basicConfig(filename='email_log.txt', level=logging.INFO)

# Function to send email with text content
def send_email(receiver_email, quality_comment, quality_reason, pdf_filename, image_filename):
    sender_email = "powerfix.electric@gmail.com"  # Sender's email address
    sender_password = read_sender_password()  # Read sender's password from a text file

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Green Coffee Beans Quality Report"

    # Text content of the email
    text_content = f"Quality Report:\n\n"
    text_content += f"Quality: {quality_comment} ({quality_reason})\n\n"
    msg.attach(MIMEText(text_content, 'plain'))

    # Attach PDF report
    with open(pdf_filename, "rb") as file:
        attach = MIMEApplication(file.read(), _subtype='pdf')
        attach.add_header('Content-Disposition', 'attachment', filename="coffee_quality_report.pdf")
        msg.attach(attach)

    # Attach image with bounding boxes
    with open(image_filename, "rb") as file:
        img = MIMEImage(file.read())
        img.add_header('Content-Disposition', 'attachment', filename="detected_image.jpg")
        msg.attach(img)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            logging.info(f'Email sent successfully to {receiver_email}')
    except Exception as e:
        logging.error(f'Error sending email: {e}')
        raise e

# Example usage:
# send_email("receiver@example.com", "High Quality", "No defects found", "report.pdf", "image_with_bounding_boxes.jpg")
