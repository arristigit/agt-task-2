from django.contrib import admin
from homeapp.models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Post)
admin.site.register(Appointment)