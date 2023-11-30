from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='home/', permanent=True)),
    path("home/", views.index, name="home"),
    path("graphics/", views.graphics, name="graphics"),
]