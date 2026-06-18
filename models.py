from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

class Registeruser(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_num = PhoneNumberField()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    pfpic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    interests = models.JSONField(default=list)

    password = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)

    verification_token = models.UUIDField(blank=True, null=True)

