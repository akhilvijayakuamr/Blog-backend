from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
from .models import CustomUser

def send_otp_mail(email):
    otp = random.randint(100000, 999999)
    sender_email = settings.EMAIL_HOST_USER
    receiver_email = email
    password_email = settings.EMAIL_HOST_PASSWORD

    subject = "Blog Master: Confirm Your Registration"

    frontend_url = f"https://blog-app-three-brown.vercel.app/verify?email={email}&otp={otp}"

    message = f"""
    <html>
    <body>
        <h2>Dear Blog Master User,</h2>
        <p>You have initiated a registration request with Blog Master.</p>
        <p><strong>Click the button below to confirm your registration:</strong></p>
        <a href="{frontend_url}" 
        style="display: inline-block; background-color: #007BFF; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;">
        Confirm Registration
        </a>
        <br><br>
        <p>If you did not request this registration, please ignore this email.</p>
        <br>
        <p>Thank you for choosing <strong>Blog Master</strong>!</p>
        <hr>
        <footer>
            <p style="font-size: 0.9em; color: gray;">If the button doesn't work, copy and paste the following URL into your browser:</p>
            <p>{frontend_url}</p>
        </footer>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        return "Failed to authenticate with the email server."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    user = CustomUser.objects.get(email=email)
    user.otp = otp
    user.save()
    return "Confirmation email sent successfully."
