from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10)
    otp_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.name
