from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.db import models


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
typePayment = (
    ("CashTrans", "Pul o'tkazmalari"),
    ("Obligation", "Obligatsiya")
)

typeStudent = (
    ("bachelor", "Bakalavr"),
    ("bagistr", "Magistr"),
)

conditions = (
    ("recieved", "Qabul qilindi"),
    ("new", "Yangi"),
    ("moderation","Moderatsiyada")
)

class Patron(TimeStapedModel):
    patron_type = models.CharField(max_length=10, choices=typeOfpatron, default=None, null=True, blank=True)
    full_name = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField('phone number', unique=True, max_length=13, 
        # validators=[PhoneValidator()]
    ) 
    condition = models.CharField(max_length=18, choices=conditions, default="moderation", null=True, blank=True)
    payment = models.FloatField(null=True, blank=True, validators=[MinValueValidator(Decimal("0.1"))])                                       #with how much money patron entered
    payment_sum = models.FloatField(null=True, blank=True, validators=[MinValueValidator(Decimal("0.1"))])                                   #sum of all payments
    payment_type = models.CharField(max_length=40, choices=typePayment, default="CashTrans", null=True, blank=True)
    name_company = models.CharField(max_length=256, null=True, blank=True)                   #if patron type is yuridik u must endter name

    def __str__(self):
        return self.full_name

class Student(TimeStapedModel):
    full_name = models.CharField(max_length=256, blank=True, null=True)
    student_type = models.CharField(max_length=18, choices=typeStudent, blank=True, null=True)
    OTM = models.ForeignKey("OTM", on_delete=models.SET_NULL, null=True)
    payed_sum = models.FloatField(null=True, blank=True, validators=[MinValueValidator(Decimal("0.1"))])
    contract_sum = models.FloatField(null=True, blank=True, validators=[MinValueValidator(Decimal("0.1"))])
    
    @property
    def must_pay(self):
        payed_sum = self.objects.aggregate(Sum('payed_sum'))
        

    def __str__(self):
        return self.full_name
        
class PatronToStudent(TimeStapedModel):
    patron = models.ForeignKey("Patron", on_delete=models.CASCADE, null=True)
    student = models.ForeignKey("Student", on_delete=models.CASCADE, null=True)
    payed = models.FloatField(null=True, default=0, validators=[MinValueValidator(Decimal("0.1"))])

    def save(self):
        pass

class OTM(TimeStapedModel):
    name = models.CharField(max_length=256, null=True)
    
    def __str__(self):
        return self.name



