import streamlit as st
import smtplib
from email.mime.text import MIMEText

# === Config ===
SECRET_TOKEN = "your-shared-token"  # Change this!
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "your-email@example.com"
SMTP_PASSWORD = "your-app-password"  # Use an app password (not your Gmail password!)

# === Get query params ===
params = st.query_params
to_email = params.get("to", [None])[0]
subject = params.get("subject", [None])[0]
body = params.get("body", [None])[0]
token = params.get("token", [None])[0]

# === Validate inputs ===
if not (to_email and subject and body and token):
    st.error("Missing one or more required query parameters: to, subject, body, token")
    st.stop()

if token != SECRET_TOKEN:
    st.error("Unauthorized: token does not match")
    st.stop()

# === Send the email ===
try:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    st.success(f"✅ Email sent to {to_email}")
except Exception as e:
    st.error(f"❌ Failed to send email: {str(e)}")
