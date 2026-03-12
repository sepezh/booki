from django.db import models
from .book import Book
from .library import Library


class LibraryBook(models.Model):
    """ Library Book model """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0)
    bookshelf = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.book} has {self.quantity} in {self.library}'
