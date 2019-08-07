from django.contrib import admin

# Register your models here.


from .models import Cuisine
#from .models import Restaurant

admin.site.register(Cuisine)
