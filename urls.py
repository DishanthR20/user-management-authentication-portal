from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('set-password/<uuid:token>/', views.set_password, name='set_password'),
    path('login/', views.login_view, name='login'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('qr-generator/', views.qr_generator, name='qr_generator'),
    path('qr-options/', views.selection, name='selection'),
    path('url-qr/', views.url_qr, name='url_qr'),
]