import random
import string
from django.db import models
from django.contrib.auth import get_user_model
from .book import Book
from .library import Library


class Reserve(models.Model):
    """Reserve model"""
    class Status(models.TextChoices):
        """Reserve model statuses"""
        PENDING = 'PE', 'Pending'
        PICKED = 'PI', 'Picked'
        BACKED = 'BA', 'Backed'
        REJECTED = 'RE', 'Rejected'
        CANCELED = 'CA', 'Canceled'
    code = models.TextField(max_length=100, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    status = models.TextField(max_length=2, choices=Status.choices, default=Status.PENDING)
    reject_at = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    until_at = models.DateTimeField(null=True, blank=True, default=None)

    def generate_unique_code(self):
        """Generate a unique code."""
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return code

    def save(self, *args, **kwargs):
        # Generate a unique code if it is not set
        if not self.code:
            code = self.generate_unique_code()
            while Reserve.objects.filter(code=code).exists():
                code = self.generate_unique_code()
            self.code = code
        super().save(*args, **kwargs)
