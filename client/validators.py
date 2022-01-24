from django.core.exceptions import ValidationError
import phonenumbers
from . import models

class PhoneValidator:
    requires_context = False
    @staticmethod
    def validate(value):
        try:
            item = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(item):
                return False
        except Exception as e:
            return False
        if len(value) != 13 or not value[1:].startswith("998"):
            return False
        return True
    def __call__(self,value):
        if not PhoneValidator.validate(value):
            raise ValidationError("Phone number invalid")