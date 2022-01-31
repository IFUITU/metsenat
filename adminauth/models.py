from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from rest_framework.validators import ValidationError


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
    payment = models.FloatField(default=0, null=True, blank=True, validators=[MinValueValidator(Decimal("0"))])                                       #with how much money patron entered
    payment_sum = models.FloatField(default=0, null=True, blank=True, validators=[MinValueValidator(Decimal("0"))])                                   #sum of all payments
    payment_type = models.CharField(max_length=40, choices=typePayment, default="CashTrans", null=True, blank=True)
    name_company = models.CharField(max_length=256, null=True, blank=True)                   #if patron type is yuridik u must endter name

    @property
    def remainder_payment(self):
        result = self.payment - self.payment_sum 
        return result

    def __str__(self):
        return self.full_name


class Student(TimeStapedModel):
    full_name = models.CharField(max_length=256, blank=True, null=True)
    student_type = models.CharField(max_length=18, choices=typeStudent, blank=True, null=True)
    OTM = models.ForeignKey("OTM", on_delete=models.SET_NULL, null=True)
    payed_sum = models.FloatField(default=0, null=True, blank=True, validators=[MinValueValidator(Decimal("0"))])
    contract_sum = models.FloatField(default=0, null=True, blank=True, validators=[MinValueValidator(Decimal("0"))])
    
    @property
    def remainder_contract(self):
        result = self.contract_sum - self.payed_sum
        return result
        

    def __str__(self):
        return self.full_name


class PatronToStudent(TimeStapedModel):
    patron = models.ForeignKey("Patron", on_delete=models.CASCADE, null=True)
    student = models.ForeignKey("Student", on_delete=models.CASCADE, null=True)
    payed = models.FloatField(null=True, default=0, validators=[MinValueValidator(Decimal("0"))])


class OTM(TimeStapedModel):
    name = models.CharField(max_length=256, null=True)
    
    def __str__(self):
        return self.name


#------------------------SIGNALS-------------------------


@receiver(pre_save, sender=PatronToStudent)
def calculate_signal(sender, instance, **kwargs):
    try:
        patron = instance.patron
        student = instance.student
    except Exception as ex:
        raise ValidationError(ex)
        
    if instance.pk:
        prev_obj = PatronToStudent.objects.get(pk=instance.pk)
        if prev_obj.student != student:
            raise ValidationError("Student can't be chnged!")

        if prev_obj.patron != instance.patron:
            prev_obj.patron.payment_sum = prev_obj.patron.payment_sum - prev_obj.payed
            prev_obj.patron.save()
        else:
            patron.payment_sum = patron.payment_sum - prev_obj.payed
            
    student.payed_sum = student.payed_sum - prev_obj.payed
    patron.payment_sum = patron.payment_sum + instance.payed
    student.payed_sum = student.payed_sum + instance.payed

    patron.save()
    student.save()


@receiver(pre_delete, sender=PatronToStudent)
def calculate_delete(sender, instance, **kwargs):
    if instance.pk:
        instance.patron.payment_sum = instance.patron.payment_sum - instance.payed
        instance.student.payed_sum = instance.student.payed_sum - instance.payed
        instance.patron.save()
        instance.student.save()
