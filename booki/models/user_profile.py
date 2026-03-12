from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from ..utils import geo


def upload_user(instance, filename):
    """Upload path for users"""
    filename = 'avatar_' + instance.user.username + filename.split('.')[1]
    return f'uploads/{instance.user.username}/{filename}'


class UserProfile(models.Model):
    """User Profile model"""
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    pic = models.ImageField(upload_to=upload_user, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True, default=None)
    latitude = models.FloatField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def get_location(self):
        """ get location long, lat"""
        if self.longitude and self.latitude:
            return self.longitude, self.latitude
        else:
            self.longitude, self.latitude = geo.get_long_lat(
                self.address,
                self.zip_code,
                self.city,
                self.country
            )
            self.save()
            return self.longitude, self.latitude


@receiver(post_save, sender=get_user_model)
def create_or_update_user_profile(_, instance, created, **kwargs):
    """Create or update User Profile for user on create method"""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()
