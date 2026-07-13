from decimal import Decimal
import random

from django.http import request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from hotel.models import Amenity, Hotel,Booking, HotelRating
from hotel.serializers import AmenitySerializer, BookingSerializer, HotelRatingSerializer, HotelSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework import mixins,generics



class AmenityAPI(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser] #IsAdminUser
    def get(self, request):
        queryset = Amenity.objects.all()
        serializer = AmenitySerializer(queryset, many=True)
        return Response({"message": "Amenities fethched", "data": serializer.data, "status" : True})

    def post(self, request):
        data = request.data
        serializer = AmenitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Amenity created successfully!", "data": serializer.data, "status" : True})
        return Response({"message": "Amenity creation failed!", "errors": serializer.errors, "status" : False})
        

    
    def put(self, request):
        data = request.data
        if data.get("id") is None:
            return Response({"message": "Amenity ID is required for update!", "status" : False})
        amenity = Amenity.objects.filter(id=data.get("id")).first()
        if amenity is None:
            return Response({"message": "Amenity not found!", "status" : False})
        serializer = AmenitySerializer(amenity, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Amenity updated successfully!", "data": serializer.data, "status" : True})
        return Response({"message": "Amenity update failed!", "errors": serializer.errors, "status" : False})
    

    def patch(self, request):
        data = request.data
        if data.get("id") is None:
            return Response({"message": "Amenity ID is required for update!", "status" : False})
        amenity = Amenity.objects.filter(id=data.get("id")).first()
        if amenity is None:
            return Response({"message": "Amenity not found!", "status" : False})
        serializer = AmenitySerializer(amenity, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Amenity patched successfully!", "data": serializer.data, "status" : True})
        return Response({"message": "Amenity patch failed!", "errors": serializer.errors, "status" : False})

    def delete(self, request):
        data = request.data
        if data.get("id") is None:
            return Response({"message": "Amenity ID is required for deletion!", "status" : False})
        amenity = Amenity.objects.filter(id=data.get("id")).first()
        if amenity is None:
            return Response({"message": "Amenity not found!", "status" : False})
        amenity.delete()
        return Response({"message": "Amenity deleted successfully!", "status" : True})
    

class AdminHotelAPI(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser] #IsAdminUser
    def get(self, request):
        queryset = Hotel.objects.all()
        serializer = HotelSerializer(queryset, many=True)
        return Response({"message": "Hotels fethched", "data": serializer.data, "status" : True})

    def generate_test_hotels(self):
        amenity_names = [
            "Free Wi-Fi", "Swimming Pool", "Spa & Wellness Centre", "Fitness Centre", 
            "Complimentary Breakfast", "Bar / Lounge", "Room Service", 
            "Valet Parking", "Airport Shuttle", "Air Conditioning"
        ]
        amenities_objects = []
        for name in amenity_names:
            amenity, _ = Amenity.objects.get_or_create(
                name=name, 
                defaults={"description": f"Standard {name.lower()} facilities available for guests."}
            )
            amenities_objects.append(amenity)

        # 2. Authentic Indian Hotel naming building blocks
        prefixes = ["The", "Royal", "Grand", "Heritage", "Imperial", "Golden", "Vista", "Taj", "Raj", "Palace", "Shree", "Sai"]
        keywords = ["Residency", "Palace", "Inn", "Resort", "Suites", "Retreat", "Manor", "Castle", "Continental", "Plaza", "Premium"]
        suffixes = ["By the River", "Classic", "International", "View", "Regency", "Comfort"]

        # Mapping of real Indian States to major Cities
        india_locations = {
            "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
            "Delhi": ["New Delhi"],
            "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubli"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Ooty"],
            "Goa": ["Panaji", "Margao", "Calangute", "Vasco da Gama"],
            "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur", "Jaisalmer"],
            "Kerala": ["Kochi", "Thiruvananthapuram", "Munnar", "Alappuzha"],
            "West Bengal": ["Kolkata", "Darjeeling", "Siliguri"],
            "Telangana": ["Hyderabad", "Warangal"],
            "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"]
        }

        streets = ["MG Road", "Link Road", "Station Road", "VIP Road", "Mall Road", "Beach Road", "Main Bazaar"]
        hotels_created = 0
        created_names = set() 

        while hotels_created < 100:
            if random.random() > 0.5:
                name = f"{random.choice(prefixes)} {random.choice(keywords)}"
            else:
                name = f"{random.choice(prefixes)} {random.choice(keywords)} {random.choice(suffixes)}"
            if name in created_names:
                name += f" {random.randint(1, 100)}"
            created_names.add(name)

            # Pick location
            state = random.choice(list(india_locations.keys()))
            city = random.choice(india_locations[state])
            
            # Fake details
            address = f"{random.randint(10, 999)}, {random.choice(streets)}, Near City Center, {city}"
            zip_code = f"{random.randint(110, 850)}{random.randint(100, 999)}" # Rough Indian 6-digit PIN code format
            phone_number = f"+91 {random.randint(700, 999)}{random.randint(100000, 999999)}"
            email = f"info@{name.lower().replace(' ', '')}.in"
            website = f"https://www.{name.lower().replace(' ', '')}.in"
            
            # Decimal values
            price = Decimal(random.randint(1500, 25000)) # Realistic INR price bounds
            rating = Decimal(round(random.uniform(3.0, 5.0), 2))
            description = f"Experience world-class luxury and Indian hospitality at {name}, located in the heart of {city}, {state}. Perfect for business and leisure travelers alike."

            # Save to database
            hotel = Hotel.objects.create(
                name=name,
                address=address,
                city=city,
                state=state,
                country="India",
                zip_code=zip_code,
                phone_number=phone_number,
                email=email,
                website=website,
                price=price,
                rating=rating,
                description=description
                # Leaving image as null/blank for basic testing
            )

            # Add random selection of amenities (between 3 to 7 amenities per hotel)
            hotel_amenities = random.sample(amenities_objects, k=random.randint(3, 7))
            hotel.amenities.set(hotel_amenities)

            hotels_created += 1

        print(f"Successfully generated {hotels_created} Indian hotels with realistic locations and amenities!")

    def post(self, request):
        data = request.data
        serializer = HotelSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Hotel created successfully!", "data": serializer.data, "status" : True})
        return Response({"message": "Hotel creation failed!", "errors": serializer.errors, "status" : False})

    
    def put(self, request):
        data = request.data
        if data.get("id") is None:
            return Response({"message": "Hotel ID is required for update!", "status" : False})
        hotel = Hotel.objects.filter(id=data.get("id")).first()
        if hotel is None:       
            return Response({"message": "Hotel not found!", "status" : False})
        serializer = HotelSerializer(hotel, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Hotel updated successfully!", "data": serializer.data, "status" : True})
        return Response({"message": "Hotel update failed!", "errors": serializer.errors, "status" : False})

    def patch(self, request):
        data = request.data
        if data.get("id") is None:
            return Response({"message": "Hotel ID is required for update!", "status" : False})
        hotel = Hotel.objects.filter(id=data.get("id")).first()
        if hotel is None:
            return Response({"message": "Hotel not found!", "status" : False})
        serializer = HotelSerializer(hotel, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Hotel patched successfully!", "data": serializer.data, "status" : True})
        return Response({"message": "Hotel patch failed!", "errors": serializer.errors, "status" : False})

    def delete(self, request):
        data = request.data
        if data.get("id") is None:      
            return Response({"message": "Hotel ID is required for deletion!", "status" : False})
        hotel = Hotel.objects.filter(id=data.get("id")).first()
        if hotel is None:
            return Response({"message": "Hotel not found!", "status" : False})
        hotel.delete()
        return Response({"message": "Hotel deleted successfully!", "status" : True})



class HotelAPI(APIView):
    def get(self, request):
        queryset = Hotel.objects.all()
        state  = request.GET.get("state")
        price = request.GET.get("price")
        price_filter = request.GET.get("price_filter", "gte")  
        _range = request.GET.get("range") 
        cities = request.GET.get("cities") 

        
        if state:
            queryset = queryset.filter(state__icontains=state)


        if price:
            if price_filter == "gte":
                queryset = queryset.filter(price__gte=price)
            elif price_filter == "lte":
                queryset = queryset.filter(price__lte=price)

        if cities:
            cities_list = cities.split(",")
            queryset = queryset.filter(city__in=cities_list)

        if _range:
            _range = _range.split(",")
            if len(_range) == 2:
                queryset = queryset.filter(price__gte=int(_range[0]), price__lte=int(_range[1]))

        serializer = HotelSerializer(queryset, many=True)
        return Response({"message": "Hotels fethched","count" : queryset.count(), "data": serializer.data, "status" : True})



class BookingAPI(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user.id)
        return Response({"message": "Bookings fethched", "data": {}, "status" : True})
    
    def post(self, request):
        user = request.user 
        data = request.data
        data['user'] = user.id
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Booking created successfully!", "data": serializer.data, "status" : True})
        return Response({"message": "Booking creation failed!", "errors": serializer.errors, "status" : False})



class HotelRatingAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        ratings = HotelRating.objects.filter(user=user)
        serializer = HotelRatingSerializer(ratings, many=True)
        return Response({"message": "Ratings fetched", "data": serializer.data, "status" : True})

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = HotelRatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Rating created successfully!", "data": serializer.data, "status" : True})
        return Response({"message": "Rating creation failed!", "errors": serializer.errors, "status" : False})



class AmenityAPIMixin(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

from rest_framework import viewsets
from rest_framework.decorators import action



class AmenityViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer





    @action(detail=False, methods=['POST'])
    def cancel_amenity(self, request):
        data = request.data
        if data.get("id") is None:
            return Response({"message": "Amenity ID is required for deletion!", "status" : False})
        amenity = Amenity.objects.filter(id=data.get("id")).first()
        if not amenity:
            return Response({"message": "Amenity not found!", "status" : False})
        #amenity.is_cancel = True
        amenity.save()
        return Response({"message": "Amenity cancelled successfully!", "status" : True})
       

    @action(detail=True, methods=['GET'], url_path='invoice')
    def invoice_amenity(self, request, pk):
        data = request.data
        if pk is None:
            return Response({"message": "Amenity ID is required for invoice!", "status" : False})
        amenity = Amenity.objects.filter(id=pk).first()
        if not amenity:
            return Response({"message": "Amenity not found!", "status" : False})
        # Logic to generate invoice for the amenity
        # For demonstration, we'll just return a success message
        return Response({"message": f"Invoice generated for Amenity ID {amenity.id}!", "status" : True})


from utility.permissions import IsManager,RoleAccess

class AmenityViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsManager]
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"count" : queryset.count(),"message": "Amenities fetched successfully", "data": serializer.data, "status" : True})

    def create(self, request, *args, **kwargs):
        
        return super().create(request, *args, **kwargs)
    

    @action(detail=False, methods=['POST'])
    def cancel_amenity(self, request):
        data = request.data
        if data.get("id") is None:
            return Response({"message": "Amenity ID is required for deletion!", "status" : False})
        amenity = Amenity.objects.filter(id=data.get("id")).first()
        if not amenity:
            return Response({"message": "Amenity not found!", "status" : False})
        #amenity.is_cancel = True
        amenity.save()
        return Response({"message": "Amenity cancelled successfully!", "status" : True})
       

    @action(detail=True, methods=['GET'], url_path='invoice')
    def invoice_amenity(self, request, pk):
        data = request.data
        if pk is None:
            return Response({"message": "Amenity ID is required for invoice!", "status" : False})
        amenity = Amenity.objects.filter(id=pk).first()
        if not amenity:
            return Response({"message": "Amenity not found!", "status" : False})
        # Logic to generate invoice for the amenity
        # For demonstration, we'll just return a success message
        return Response({"message": f"Invoice generated for Amenity ID {amenity.id}!", "status" : True})