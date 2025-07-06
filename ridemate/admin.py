from django.contrib import admin
from .models import Ride, RideFeedback, Testimonial

# Register your models here.
admin.site.register(Ride)
admin.site.register(RideFeedback)
admin.site.register(Testimonial)
