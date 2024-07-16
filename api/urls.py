from django.urls import path
from . import views
from .views import RegisterView,LoginView,LogoutView

urlpatterns = [
    path('getbooks/',views.getBooks),
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('reserve/',views.checkAvailability)
]