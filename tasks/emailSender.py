import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Imperial College credentials
EMAIL_ADDRESS = "your.email@imperial.ac.uk"  # Replace with your email
EMAIL_PASSWORD = "your_password"  # Replace with your password

# Email content
to_email = "recipient@example.com"  # Replace with recipient's email
subject = "Your Subject Here"
body = "This is the body of the email."

# Set up the MIME
message = MIMEMultipart()
message['From'] = EMAIL_ADDRESS
message['To'] = to_email
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Send the email
try:
    # Connect to Imperial College's SMTP server
    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(message)
        print("Email sent successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
