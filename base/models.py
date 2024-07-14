from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.
class Customer(AbstractUser):
    firstname = models.TextField(default="null")
    lastname = models.TextField(default="null")
    email = models.EmailField(unique=True)
    password = models.TextField()
    phone = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__():
        return self.email

class Book(models.Model):
    title = models.TextField()
    author = models.TextField()
    publisher = models.TextField()
    img = models.TextField()

    def __str__():
        return self.title

class Timeslot(models.Model):
    start = models.DateField()
    end = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__():
        return f"Book: {self.book.title} - user:{self.customer.firstname} - start:{self.start} - end:{self.end}"
        