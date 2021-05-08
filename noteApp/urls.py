from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),    
    path('login', login, name='login'),
    path('logout', logout, name='logout'),    
    path('notelist', list_notes, name='notelist'),
    path('addnote', add_note, name='addnote'),
    path('deletenote', delete_note, name='deletenote'),
    path('updatenote', update_note, name='updatenote'),
    path('detailnote', detail_note, name='detailnote'),
    path('search', search_page, name='search_page'),
    path('searchnote', search_note, name='search_note')
]