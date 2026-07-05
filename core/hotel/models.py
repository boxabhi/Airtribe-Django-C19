from django.db import models
from utility.models import BaseModel
from django.contrib.auth.models import User


class Amenity(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Amenity - {self.name}"

class Hotel(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='hotel_images/', null=True, blank=True)
    amenities = models.ManyToManyField(Amenity, related_name='hotels', blank=True)


    def __str__(self):
        return f"Hotel - {self.name} | City : {self.city}"


class HotelRating(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Rating - {self.hotel.name} | User : {self.user.username} | Rating : {self.rating}"

class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking - {self.user.username} | Hotel : {self.hotel.name} | Check-in : {self.check_in_date} | Check-out : {self.check_out_date}"