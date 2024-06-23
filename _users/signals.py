from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            profile_owner = user,
            email = user.email
            )
        try:
            profile.firstName, profile.lastName = user.first_name.split()
        except:
            profile.firstName = user.first_name
        profile.save()

post_save.connect(createProfile, sender=User)