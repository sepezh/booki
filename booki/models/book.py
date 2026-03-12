"""import libs"""
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from .author import Author
from .category import Category
from .tag import Tag

def upload_pic(instance, filename):
    """Upload pic"""
    filename =  slugify(instance.title) + '.' + filename.split('.')[1]
    return f'uploads/{filename}'

class Book(models.Model):
    """Book model"""
    isbn = models.CharField(max_length=100, unique=True)
    authors = models.ManyToManyField(Author)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    pic = models.ImageField(upload_to=upload_pic)
    summary = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute url"""
        return reverse('book_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'
