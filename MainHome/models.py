from django.core.mail import EmailMessage

from django.db import models
from datetime import datetime, timedelta
from pyotp import TOTP

from MainUsers.models import User


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=datetime.now() + timedelta(minutes=5))

    def is_valid(self):
        return self.expires_at > datetime.now()

    def generate_otp(self):
        self.otp = TOTP('secret-key').now()
        self.save()

    def send_otp(self):
        if not self.otp:
            self.generate_otp()
        subject = 'OTP Validation of ConnectionHub'
        body = f'Dear User, use this One Time Password ({self.otp}) to register to your (ConnectionHub) account.' \
               ' This OTP will be valid for the next 5 mins.'
        message = EmailMessage(
            subject=subject,
            body=body,
            to=[self.email],
        )
        message.send()

