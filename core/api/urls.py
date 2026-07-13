"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import (create_employee_api, department_api, employee_api, example_api, login_api, logout_api, register_api)
from hotel.views import (AmenityAPI, AdminHotelAPI,
                          HotelAPI,BookingAPI,HotelRatingAPI,AmenityViewset)
from rest_framework import routers



router = routers.SimpleRouter()
router.register(r'amenities', AmenityViewset)


urlpatterns = [
    path('departments/', department_api, name='department_api'),
    path('employees/', employee_api, name='employee_api'),
    path('create-employee/', create_employee_api, name='create_employee_api'),
    path('register/', register_api, name='register_api'),
    path('login/', login_api, name='login_api'),
    path('admin/hotels/', AdminHotelAPI.as_view(), name='admin_hotel_api'),
    #path('amenities/', AmenityAPI.as_view(), name='amenity_api'),
    path('hotels/', HotelAPI.as_view(), name='hotel_api'),
    path('bookings/', BookingAPI.as_view(), name='booking_api'),
    path('ratings/', HotelRatingAPI.as_view(), name='hotel_rating_api'),
    path('logout/', logout_api, name='logout_api'),
    #path('amenity-mixin/', AmenityAPIMixin.as_view(), name='amenity_api_mixin'),
    path('api-view/', example_api, name='api_view'),
]


urlpatterns += router.urls