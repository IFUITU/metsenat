from rest_framework.validators import ValidationError

def vlidate_student(obj, new_obj, **kwargs):
    if obj != new_obj:
        raise ValidationError("Student can't be chnged!")
        