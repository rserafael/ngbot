from django.urls import path
from . import views

urlpatterns = [
    path(route='testmodels/', view=views.modelstest),
]