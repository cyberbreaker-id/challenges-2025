from django.urls import path
from . import views

urlpatterns = [
    path('api/user/login', views.user_login, name='user_login'),
    path('api/user/register', views.user_register, name='user_register'),
    path('api/notes', views.notes_list, name='notes_list'),
    path('api/debug', views.debug, name='debug'),
]