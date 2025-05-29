import streamlit as st
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText

# Shared encryption key and token
ENCRYPTION_KEY = b'MY_GENERATED_SECRET_KEY'
SECRET_TOKEN = "YOUR_SECRET_TOKEN"
fernet = Fernet(ENCRYPTION_KEY)

# Parse query params
params = st.experimental_get_query_params()

to_email = params.get("to", [None])[0]
subject = params.get("subject", [None])[0]
encrypted_body = params.get("body", [None])[0]
token = params.get("token", [None])[0]

if not (to_email and subject and encrypted_body and token):
    st.warning("Missing required query parameters.")
    st.stop()

if token != SECRET_TOKEN:
    st.error("Unauthorized request.")
    st.stop()

try:
    body = fernet.decrypt(encrypted_body.encode()).decode()

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "your-email@example.com"
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("your-email@example.com", "your-app-password")
        server.send_message(msg)

    st.success(f"Email sent to {to_email}")
except Exception as e:
    st.error(f"Error sending email: {str(e)}")
