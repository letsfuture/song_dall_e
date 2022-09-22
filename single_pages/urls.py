from django.urls import path
from . import views

urlpatterns = [
    # path('create/', views.SummaryCreate.as_view()),
    path('about_us/', views.about_us),
    path('how_to_use/', views.how_to_use),
    path('create/', views.predict_model, name='predict_model'),
    path('', views.landing),
]