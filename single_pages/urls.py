from django.urls import path
from . import views

urlpatterns = [
    path('about_us/', views.about_us),
    path('how_to_use/', views.how_to_use),
    path('create/', views.create),
    path('', views.landing),
]