import streamlit as st
import smtplib
import json
from email.mime.text import MIMEText

st.set_page_config(page_title="Email API")

if st.request.method == "POST":
    try:
        data = json.loads(st.request.body.decode("utf-8"))
        to_email = data["to"]
        subject = data["subject"]
        body = data["body"]

        # Send email (you can use Gmail SMTP or any service like SendGrid)
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = "your-email@example.com"
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("your-email@example.com", "your-app-password")
            server.send_message(msg)

        st.json({"status": "success", "message": "Email sent successfully"})
    except Exception as e:
        st.json({"status": "error", "message": str(e)})

else:
    st.write("POST email data to this endpoint.")
