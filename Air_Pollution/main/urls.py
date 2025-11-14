from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("air_history/", views.air_history, name="air_history"),
]

