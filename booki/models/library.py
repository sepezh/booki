from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ..utils import geo


class Library(models.Model):
    """Library model"""
    staff = models.ManyToManyField(get_user_model())
    slug = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    longitude = models.FloatField(null=True, blank=True, default=None)
    latitude = models.FloatField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
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

    def get_address(self):
        """ get address """
        return f'{self.address}, {self.zip_code} {self.city}, {self.country}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
