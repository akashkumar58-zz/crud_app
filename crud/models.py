from django.db import models

# Create your models here.

class Book(models.Model):
    """
    Book Model - defining the attributes
    """
    isbn = models.CharField(max_length=10)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)

    def get_author(self):
        return self.title + ' is written by ' + self.author + '.'

    def __repr__(self):
        return self.title + ' is added.'

