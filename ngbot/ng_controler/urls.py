from django.urls import path
from . import views

urlpatterns = [
    path(route='testmodels/', view=views.models_test),
    path(route='showrequest/', view=views.request_show),
    path(route='resetngacc/<str:pwd>/', view=views.reset_all_instagram_accounts)
]
