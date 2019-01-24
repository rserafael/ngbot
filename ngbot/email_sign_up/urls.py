from django.urls import path
from . import views

urlpatterns = [
    path(route='outlook/<str:name>/<str:lastname>/<int:year>/', view=views.create_outlook_email)
]