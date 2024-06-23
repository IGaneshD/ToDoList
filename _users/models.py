from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.
class Profile(models.Model):
    profile_owner = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    firstName = models.CharField(max_length=50, null=True, blank=True)
    lastName = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(blank_label="(Select country)", blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    email_verified = models.BooleanField(verbose_name="is email Verified", default=False, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    onboarding_done = models.BooleanField(default=False, verbose_name="is onboarded", blank=True, null=True )
    # p_image = models.ImageField((""), upload_to=None, height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return f'{self.profile_owner.username}'
