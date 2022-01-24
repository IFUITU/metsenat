from email.mime import application
from hashlib import new
from pyexpat import model
from random import choices
from django.db import models
from client.validators import PhoneValidator
# Create your models here.
class TimeStapedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

typeOfpatron = (
    ("Jismoniy", "Jismoniy"),
    ("Yuridik", "Yuridik"),
)
conditinos = (
    ("recieved", "Qabul qilindi"),
    ("new", "Yangi")
)

class Application(TimeStapedModel):
    condition = models.CharField(max_length=40, choices=conditinos, default=None, null=True, blank=True)
    patron_type = models.CharField(max_length=10, choices=typeOfpatron, default=None, null=True, blank=True)
    full_name = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField('phone number', unique=True, max_length=13, 
        # validators=[PhoneValidator()]
    )
    payment = models.FloatField(null=True, blank=True)
    name_company = models.CharField(max_length=256, null=True, blank=True)