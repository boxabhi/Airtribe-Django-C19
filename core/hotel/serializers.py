from rest_framework import serializers
from .models import Amenity, Hotel, HotelRating, Booking



class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        if Amenity.objects.filter(name=value).exists():
            raise serializers.ValidationError("Amenity with this name already exists.")
        return value


class HotelSerializer(serializers.ModelSerializer):
    #amenities = AmenitySerializer(many=True, read_only=True)
    amenities_data = serializers.PrimaryKeyRelatedField(queryset=Amenity.objects.all(), many=True, write_only=True, source='amenities')
    #amenities_data = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    class Meta:
        model = Hotel
        exclude = ['rating', 'created_at', 'updated_at','amenities']


    def validate_state(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("State must contain only alphabetic characters.")
        return value

    def create(self, validated_data):
        amenities_data = validated_data.pop('amenities', [])
        hotel = Hotel.objects.create(**validated_data)
        for amenity_data in amenities_data:
            hotel.amenities.add(amenity_data)
        return hotel


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'hotel', 'check_in_date', 'check_out_date', 'number_of_guests','total_price']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['hotel'] = HotelSerializer(instance.hotel).data
        # data.pop('user')  
        return data


    def validate(self, data):
        if data['check_in_date'] >= data['check_out_date']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")

        if Booking.objects.filter(hotel=data['hotel'],check_in_date__lt=data['check_out_date'],check_out_date__gt=data['check_in_date']).exists():
            raise serializers.ValidationError("The hotel is already booked for the selected dates.")
        
        return data


class HotelRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRating
        fields = ['id', 'hotel', 'user', 'rating', 'review', 'is_published', 'is_abusive']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['hotel'] = HotelSerializer(instance.hotel).data
        # data.pop('user')  
        return data