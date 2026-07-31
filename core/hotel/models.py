from decimal import Decimal
import re
from django.core.exceptions import ValidationError
from django.db import models
from utility.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save, pre_delete, post_delete
from django.dispatch import receiver
class Amenity(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Amenity - {self.name}"

    def clean(self):
        if self.name and len(self.name) > 50:
            raise ValidationError("Amenity name cannot exceed 50 characters.")

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
    is_published = models.BooleanField(default=False)
    is_abusive = models.BooleanField(default=False)

    def __str__(self):
        return f"Rating - {self.hotel.name} | User : {self.user.username} | Rating : {self.rating}"

class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking - {self.user.username} | Hotel : {self.hotel.name} | Check-in : {self.check_in_date} | Check-out : {self.check_out_date}"


@receiver(pre_save, sender=Booking)
def calculate_booking_total_price(sender, instance, **kwargs):
    if not instance.hotel_id:
        return
    if not instance.check_in_date or not instance.check_out_date:
        return
    total_days = (instance.check_out_date - instance.check_in_date).days
    if total_days <= 0:
        instance.total_price = Decimal("0.00")
        return

    instance.total_price = instance.hotel.price * total_days


@receiver(post_save, sender=HotelRating)
def moderate_hotel_rating(sender, instance, created, **kwargs):
    ABUSIVE_WORDS = {
        "bad",
        "poor",
        "terrible",
        "awful",
        "horrible",
    }
    review = instance.review or ""
    words = set(re.findall(r"\b\w+\b", review.lower()))
    contains_abusive_word = bool(words.intersection(ABUSIVE_WORDS))
    expected_is_abusive = contains_abusive_word
    expected_is_published = not contains_abusive_word
    if (instance.is_abusive != expected_is_abusive or instance.is_published != expected_is_published ):
        HotelRating.objects.filter(pk=instance.pk).update(
            is_abusive=expected_is_abusive,
            is_published=expected_is_published,
        )