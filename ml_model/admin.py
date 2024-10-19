from django.contrib import admin
from .models import Schedule
from .models import Predicted_Schedule
from .models import Item

# Register your models here.


admin.site.register(Schedule)
admin.site.register(Predicted_Schedule)
admin.site.register(Item)