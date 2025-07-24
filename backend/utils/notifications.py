import os
import smtplib
from email.mime.text import MIMEText
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from twilio.rest import Client as TwilioClient

# --- Email Notification ---
def send_email_notification(subject, body, to_email):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    from_email = os.getenv("FROM_EMAIL", smtp_user)
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, [to_email], msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Email notification failed: {e}")

# --- Slack Notification ---
def send_slack_notification(message, channel=None):
    slack_token = os.getenv("SLACK_TOKEN")
    slack_channel = channel or os.getenv("SLACK_CHANNEL")
    if not slack_token or not slack_channel:
        print("Slack token or channel not set.")
        return
    client = WebClient(token=slack_token)
    try:
        client.chat_postMessage(channel=slack_channel, text=message)
        print(f"Slack message sent to {slack_channel}")
    except SlackApiError as e:
        print(f"Slack notification failed: {e.response['error']}")

# --- SMS Notification (Twilio) ---
def send_sms_notification(body, to_number):
    twilio_sid = os.getenv("TWILIO_SID")
    twilio_token = os.getenv("TWILIO_TOKEN")
    from_number = os.getenv("TWILIO_FROM")
    if not twilio_sid or not twilio_token or not from_number:
        print("Twilio credentials not set.")
        return
    client = TwilioClient(twilio_sid, twilio_token)
    try:
        client.messages.create(body=body, from_=from_number, to=to_number)
        print(f"SMS sent to {to_number}")
    except Exception as e:
        print(f"SMS notification failed: {e}")

# --- Unified Notification Router ---
def send_notification(subject, body, channels=["email", "slack"], to_email=None, slack_channel=None, to_number=None):
    if "email" in channels and to_email:
        send_email_notification(subject, body, to_email)
    if "slack" in channels:
        send_slack_notification(f"{subject}\n{body}", channel=slack_channel)
    if "sms" in channels and to_number:
        send_sms_notification(body, to_number) 