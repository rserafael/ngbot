from django.urls import path
from . import views

urlpatterns = [
    path(route='outlook/', view=views.create_outlook_email),
    path(route='getverificationimage/<str:img_url>/<str:driver_key>/', view=views.get_verification_image, name='get_verification_image'),
]