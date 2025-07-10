from django.urls import path
from .views import (
    WatchItemCreateView , WatchItemDetailView , WatchItemDeleteView , 
    WatchItemListView , WatchItemUpdateView , MovieSearchView , 
    AddFromAPIView
)



urlpatterns = [
    path('', WatchItemListView.as_view(), name= 'home'),
    path('item/<int:pk>/', WatchItemDetailView.as_view(), name='details'),
    path('add/', WatchItemCreateView.as_view(), name='add_item'),
    path('item/<int:pk>/edit/', WatchItemUpdateView.as_view(), name='edit_item'),
    path('item/<int:pk>/delete/', WatchItemDeleteView.as_view(), name='delete_item'),
    path('search/', MovieSearchView.as_view(), name='movie_search'),
    path('add-from-api/', AddFromAPIView.as_view(), name='add_from_api'),
]


#This urls.py connects all pages (home, details, add, edit, delete) to  views, so Django knows which code to run for each URL.

