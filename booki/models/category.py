from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """Category model"""
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute url"""
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'
