from django.db import models

# Create your models here.

class Daraz(models.Model):
    brand = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    # category = models.CharField(max_length=100)
    original = models.CharField(max_length=100)
    discount = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class SastoDeal(models.Model):
    brand = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    original = models.CharField(max_length=100)
    discount = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Hamrobazar(models.Model):
    title = models.CharField(max_length=100)
    price= models.CharField(max_length= 100)