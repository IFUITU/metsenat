from .models import Student, Patron
from rest_framework.validators import ValidationError
def calculate(obj, **kwargs):
    try:
        student = Student.objects.get(id=obj['student'])
        patron = Patron.objects.get(id=obj['patron'])
        prev_obj = kwargs.pop('prev_obj', None)
    except Exception as ex:
        raise ValidationError(ex)
    
    if prev_obj != None and prev_obj.patron != patron:
        prev_obj.patron.payment_sum = prev_obj.patron.payment_sum - prev_obj.payed
        student.payed_sum = student.payed_sum - prev_obj.payed
        prev_obj.patron.save()
    elif prev_obj != None:
        student.payed_sum = student.payed_sum - prev_obj.payed
        patron.payment_sum = patron.payment_sum - prev_obj.payed

    patron.payment_sum = patron.payment_sum + obj['payed']
    student.payed_sum = student.payed_sum + obj['payed']
    patron.save()
    student.save()
