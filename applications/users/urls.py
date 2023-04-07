from django.urls import path, include
from .views import RegistrationView, ActivationView, LoginView, LogoutView


urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('activation/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
]
# admin, 1 -> oijasdojif9230d232dlk




