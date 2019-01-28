from django.urls import path
from . import views

urlpatterns = [
    path(route='outlook/', view=views.create_outlook_email),
    path(route='getverfimg/<str:img_key>/', view=views.get_verification_image, name='get_verf_img'),
    path(route='setverftext/<str:verification_text>/', view=views.set_verification_text, name='set_verf_text'),
    path(route='getverftext/', view=views.get_verification_text, name="get_verf_text")
]