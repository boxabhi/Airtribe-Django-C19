from django.contrib import admin

# Register your models here.
from hotel.models import Amenity, Hotel, HotelRating, Booking

admin.site.register(Amenity)
admin.site.register(Hotel)
admin.site.register(HotelRating)
admin.site.register(Booking)
