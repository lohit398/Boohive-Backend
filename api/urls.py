from django.urls import path
from . import views
from .views import RegisterView,LoginView

urlpatterns = [
    path('getbooks/',views.getBooks),
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('reserve/',views.reserveBook)
]