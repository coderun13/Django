from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_book(self):
        return Book.objects.filter(author=self)

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    website = models.URLField()

    def __str__(self):
        return self.name
    
    def formated_address(self):
        return f"{self.address}, {self.city}, {self.state_province} {self.country}"
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title
    
    def book_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.publication_date.year