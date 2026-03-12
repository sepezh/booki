import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def upload_pic(instance, filename) -> str:
    """Upload pic"""
    filename = slugify(f'{instance.first_name}-{instance.last_name}') + '-' + str(uuid.uuid4()) + '.' + filename.split('.')[1]
    return f'uploads/{filename}'


class Author(models.Model):
    """Author model"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    pic = models.ImageField(upload_to=upload_pic)
    summary = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        """Get absolute url"""
        slug_val = slugify(f'{self.id}-{self.first_name}-{self.last_name}')
        return reverse('author_detail', kwargs={'slug': slug_val})

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
