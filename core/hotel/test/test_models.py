from django.test import TestCase
from hotel.models import Amenity, Hotel, HotelRating, Booking


class AmenityModelTestCase(TestCase):

    def setUp(self):            
       self.amenity = Amenity.objects.create(name="Free Wi-Fi", description="High-speed wireless internet access.")

    # def test_amenity_creation(self):
    #     self.assertEqual(self.amenity.name, "Free Wi-Fi")
    #     self.assertEqual(self.amenity.description, "High-speed wireless internet access.")

    # def test_amenity_name_max_length(self):
    #     self.amenity.name = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride Printing Library in London, took a 1914 Cicero translation and scrambled it to make dummy text for Letraset's Body Type sheets."
    #     self.assertRaises(Exception, self.amenity.save)