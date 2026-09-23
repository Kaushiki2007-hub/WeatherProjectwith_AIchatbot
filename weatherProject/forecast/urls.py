from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_view, name='Weather View'),
    path("ai-chat/", views.ai_chat, name="ai_chat"),
]
