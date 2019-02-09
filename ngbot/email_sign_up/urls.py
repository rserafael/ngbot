from django.urls import path
from . import views

urlpatterns = [
    path(route='outlook/create/', view=views.create_outlook_email),
    path(route='outlook/getverfimg/', view=views.get_verification_image, name='get_verf_img'),
    path(route='outlook/setverftext/<str:verification_text>/', view=views.set_verification_text, name='set_verf_text'),
    path(route='outlook/getverftext/', view=views.get_verification_text, name="get_verf_text"),
    path(route="outlook/people/", view=views.all_outlook_people),
    path(route="outlook/emailvalidation/", view=views.who_can_log_in)
]