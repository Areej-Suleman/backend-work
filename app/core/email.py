"""
Email service for sending verification emails and other notifications
"""

import smtplib
import secrets
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from jinja2 import Template

from app.core.config import settings


class EmailService:
    """Email service for sending various types of emails"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
        self.from_name = settings.FROM_NAME
        self.frontend_url = settings.FRONTEND_URL
    
    def _get_smtp_connection(self):
        """Get SMTP connection"""
        if not self.smtp_username or not self.smtp_password:
            raise ValueError("Email credentials not configured. Please set SMTP_USERNAME and SMTP_PASSWORD")
        
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.starttls()
        server.login(self.smtp_username, self.smtp_password)
        return server
    
    def _send_email(self, to_email: str, subject: str, html_content: str, text_content: Optional[str] = None):
        """Send email with HTML content"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text version if provided
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML version
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with self._get_smtp_connection() as server:
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_verification_email(self, to_email: str, full_name: str, verification_token: str) -> bool:
        """Send email verification email"""
        verification_url = f"{self.frontend_url}/verify-email?token={verification_token}"
        
        # HTML template
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email - GlowGenius</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                .button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .button:hover { background: #5a6fd8; }
                .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
                .warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🌟 Welcome to GlowGenius!</h1>
            </div>
            <div class="content">
                <h2>Hi {{ full_name }}!</h2>
                <p>Thank you for signing up for GlowGenius! We're excited to help you on your beauty journey.</p>
                <p>To get started, please verify your email address by clicking the button below:</p>
                
                <div style="text-align: center;">
                    <a href="{{ verification_url }}" class="button">✓ Verify My Email</a>
                </div>
                
                <div class="warning">
                    <strong>Important:</strong> This verification link will expire in 24 hours for security reasons.
                </div>
                
                <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background: #f0f0f0; padding: 10px; border-radius: 5px;">
                    {{ verification_url }}
                </p>
                
                <h3>What's next?</h3>
                <p>Once you verify your email, you'll be able to:</p>
                <ul>
                    <li>🤳 Upload photos for skin analysis</li>
                    <li>💄 Get personalized product recommendations</li>
                    <li>💬 Chat with our AI beauty assistant</li>
                    <li>⏰ Set skincare reminders</li>
                    <li>📊 Track your beauty progress</li>
                </ul>
                
                <p>If you didn't create an account with GlowGenius, you can safely ignore this email.</p>
            </div>
            <div class="footer">
                <p>© 2024 GlowGenius. All rights reserved.</p>
                <p>This is an automated email. Please don't reply to this address.</p>
            </div>
        </body>
        </html>
        """)
        
        # Text version
        text_content = f"""
        Welcome to GlowGenius!
        
        Hi {full_name}!
        
        Thank you for signing up for GlowGenius! 
        
        To verify your email address, please visit:
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account with GlowGenius, you can safely ignore this email.
        
        © 2024 GlowGenius. All rights reserved.
        """
        
        html_content = html_template.render(
            full_name=full_name,
            verification_url=verification_url
        )
        
        return self._send_email(
            to_email=to_email,
            subject="🌟 Verify Your Email - Welcome to GlowGenius!",
            html_content=html_content,
            text_content=text_content
        )
    
    def send_verification_success_email(self, to_email: str, full_name: str) -> bool:
        """Send email verification success notification"""
        login_url = f"{self.frontend_url}/login"
        
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Verified - GlowGenius</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                .button { display: inline-block; background: #00b09b; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎉 Email Verified Successfully!</h1>
            </div>
            <div class="content">
                <div class="success">
                    <strong>✓ Success!</strong> Your email has been verified successfully.
                </div>
                
                <h2>Hi {{ full_name }}!</h2>
                <p>Congratulations! Your email has been verified and your GlowGenius account is now fully activated.</p>
                
                <div style="text-align: center;">
                    <a href="{{ login_url }}" class="button">🚀 Start Your Beauty Journey</a>
                </div>
                
                <h3>You now have access to:</h3>
                <ul>
                    <li>🤳 AI-powered skin analysis</li>
                    <li>💄 Personalized product recommendations</li>
                    <li>💬 Beauty chatbot assistance</li>
                    <li>⏰ Skincare routine reminders</li>
                    <li>📊 Progress tracking</li>
                </ul>
                
                <p>Ready to discover your perfect beauty routine? Log in now and let's get started!</p>
            </div>
            <div class="footer">
                <p>© 2024 GlowGenius. All rights reserved.</p>
            </div>
        </body>
        </html>
        """)
        
        html_content = html_template.render(
            full_name=full_name,
            login_url=login_url
        )
        
        text_content = f"""
        Email Verified Successfully!
        
        Hi {full_name}!
        
        Congratulations! Your email has been verified and your GlowGenius account is now fully activated.
        
        You can now log in at: {login_url}
        
        © 2024 GlowGenius. All rights reserved.
        """
        
        return self._send_email(
            to_email=to_email,
            subject="🎉 Email Verified - Welcome to GlowGenius!",
            html_content=html_content,
            text_content=text_content
        )
    
    def send_password_reset_email(self, to_email: str, full_name: str, reset_token: str) -> bool:
        """Send password reset email"""
        reset_url = f"{self.frontend_url}/reset-password?token={reset_token}"
        
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Your Password - GlowGenius</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                .button { display: inline-block; background: #f5576c; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔐 Password Reset Request</h1>
            </div>
            <div class="content">
                <h2>Hi {{ full_name }}!</h2>
                <p>We received a request to reset your GlowGenius password. If you made this request, click the button below:</p>
                
                <div style="text-align: center;">
                    <a href="{{ reset_url }}" class="button">🔑 Reset My Password</a>
                </div>
                
                <div class="warning">
                    <strong>Security Note:</strong> This reset link will expire in 1 hour for your security.
                </div>
                
                <p>If the button doesn't work, copy and paste this link:</p>
                <p style="word-break: break-all; background: #f0f0f0; padding: 10px; border-radius: 5px;">
                    {{ reset_url }}
                </p>
                
                <p><strong>If you didn't request this password reset, please ignore this email.</strong> Your password will remain unchanged.</p>
            </div>
            <div class="footer">
                <p>© 2024 GlowGenius. All rights reserved.</p>
            </div>
        </body>
        </html>
        """)
        
        html_content = html_template.render(
            full_name=full_name,
            reset_url=reset_url
        )
        
        return self._send_email(
            to_email=to_email,
            subject="🔐 Reset Your GlowGenius Password",
            html_content=html_content
        )


def generate_verification_token() -> str:
    """Generate a secure verification token"""
    return secrets.token_urlsafe(32)


def get_verification_expires() -> datetime:
    """Get verification token expiration time"""
    return datetime.utcnow() + timedelta(hours=settings.VERIFICATION_TOKEN_EXPIRE_HOURS)


# Global email service instance
email_service = EmailService()
