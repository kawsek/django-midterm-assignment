from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Car)
admin.site.register(models.Comment)
admin.site.register(models.Order)

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ['name', 'slug']
admin.site.register(models.Brand, BrandAdmin)

