from django.db import models

# Create your models here.

# certificates/models.py
from django.db import models

from .utils import generate_jwt_token
import random
import string

from django.db import models
from django.contrib.auth.models import User
# from myapp.models import Certificate

class VerificationID(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    certificate = models.ForeignKey('myapp.Certificate', on_delete=models.CASCADE)
    verification_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.verification_id

    def generate_verification_id(self):
        # Generate a random alphanumeric verification ID
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(10))

    def save(self, *args, **kwargs):
        # If it's a new object, generate the verification_id and associate it with the user
        if not self.pk:
            self.verification_id = self.generate_verification_id()

            # Save the related object 'certificate'
            self.user.save()

        super().save(*args, **kwargs)


class Certificate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    jwt_token = models.CharField(max_length=255, null=True, blank=True)

    def generate_verification_id(self):
        # Generate a random alphanumeric verification ID
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(10))

    def save(self, *args, **kwargs):
        if not self.pk:
            # Save the Certificate object to generate a primary key (ID)
            super().save(*args, **kwargs)

            # Generate a verification ID for the user
            verification_id = self.generate_verification_id()

            # Create a new VerificationID object and associate it with the user and certificate
            user = User.objects.create(username=verification_id)
            VerificationID.objects.create(user=user, verification_id=verification_id, certificate=self)

    def __str__(self):
        return self.name
    


class CertificateFile(models.Model):
    certificate = models.OneToOneField(Certificate, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='certificates/pdfs/')


from django.db import models
from django.contrib.auth.models import User
from myapp.models import Certificate

class VerificationID(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_id = models.CharField(max_length=20, unique=True)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    def __str__(self):
        return self.verification_id
