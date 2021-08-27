from django.urls import path
from . import views


urlpatterns = [
    path('', views.movie_recommendation_view, name = "recommendation")
    # route is a string contains a URL pattern
]
