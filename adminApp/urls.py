from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path(r'adminLogin', adminLogin, name='adminLogin'),
    path(r'logout', adminLogout, name='adminLogout'),
    path(r'newUserPage', newUserPage, name='newUserPage'),
    path(r'createNewUser', createNewUser, name='createNewUser'),
    path(r'dashboard', adminDashboard, name='adminDashboard'),
    path(r'deletenote', delete_note, name="deletenote"),
    path(r'deleteuser', delete_user, name="deleteuser")
]