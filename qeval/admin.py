from django.contrib import admin
from . models import c_questiondetails
from . models import py_questiondetails
from . models import java_questiondetails
# Register your models here.
admin.site.register(c_questiondetails)
admin.site.register(py_questiondetails)
admin.site.register(java_questiondetails)