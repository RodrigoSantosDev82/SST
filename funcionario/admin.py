from django.contrib import admin
from .models import Funcionario, Cargo

# Register your models here.
admin.site.register(Funcionario)
admin.site.register(Cargo)

