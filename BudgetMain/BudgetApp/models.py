from django.db import models

# Create your models here.

class Income(models.Model):
    name = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()

class Expenses(models.Model):
    name = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)

class Savings(models.Model):
    name = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()

class Withdraw_Savings(models.Model):
    name = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.amount}"