from django.urls import path
from .views import *

urlpatterns = [
    path('', user_list, name='user_list'),
    path('delete/<int:id>/', delete_user, name='delete_user'),
    path('add-user/', add_user, name='add_user'),
    path('update/<int:id>/', update_user, name='update_user'),
    path('login/', admin_login, name='admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
    path('create-admin/', create_admin, name='create_admin'),
    path('user-qr/<int:id>/', user_qr, name='user_qr'),
]