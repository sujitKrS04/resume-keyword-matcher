"""Test email sending"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

smtp_email = os.getenv("SMTP_EMAIL", "")
smtp_password = os.getenv("SMTP_PASSWORD", "")

print(f"SMTP Email: {smtp_email}")
print(f"SMTP Password: {'*' * len(smtp_password)} ({len(smtp_password)} chars)")

try:
    # Test connection
    print("\n1. Testing SMTP connection...")
    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
    print("   ✅ Connected to smtp.gmail.com:587")

    server.starttls()
    print("   ✅ TLS started")

    server.login(smtp_email, smtp_password)
    print("   ✅ Login successful")

    # Send test email
    print("\n2. Sending test email...")
    msg = MIMEMultipart()
    msg["From"] = smtp_email
    msg["To"] = smtp_email  # Send to yourself
    msg["Subject"] = "Test Email from Resume Matcher"

    body = "This is a test email from Resume Keyword Matcher. If you receive this, email is working!"
    msg.attach(MIMEText(body, "plain"))

    server.send_message(msg)
    print(f"   ✅ Test email sent to {smtp_email}")

    server.quit()
    print("\n✅ ALL TESTS PASSED!")

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback

    traceback.print_exc()
