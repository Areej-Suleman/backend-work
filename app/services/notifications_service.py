import smtplib
from email.message import EmailMessage
from app.core.config import settings
from sqlalchemy.orm import Session
from app.core.db import get_db
from app import crud

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = settings.EMAILS_FROM_EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def send_morning_reminder():
    db: Session = next(get_db()) # Get a database session
    users = crud.users.get_all(db) # Assuming get_all fetches all users
    
    subject = "Good Morning! Your Daily Skincare Reminder"
    body = "Good morning! Don't forget to cleanse, tone, and moisturize your skin. Have a glowing day!"
    
    for user in users:
        if user.email: # Ensure user has an email
            send_email(user.email, subject, body)
    db.close() # Close the session

def send_evening_reminder():
    db: Session = next(get_db()) # Get a database session
    users = crud.users.get_all(db) # Assuming get_all fetches all users
    
    subject = "Good Evening! Your Nightly Skincare Reminder"
    body = "Good evening! Remember to cleanse your face thoroughly and apply your nightly treatments before bed. Sweet dreams!"
    
    for user in users:
        if user.email: # Ensure user has an email
            send_email(user.email, subject, body)
    db.close() # Close the session
