from django.contrib import admin
from .models import Patron, OTM, Student, PatronToStudent
# Register your models here.

admin.site.register(Patron)
admin.site.register(OTM)
admin.site.register(Student)
admin.site.register(PatronToStudent)