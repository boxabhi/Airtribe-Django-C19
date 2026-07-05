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

