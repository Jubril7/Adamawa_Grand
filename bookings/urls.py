from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:room_pk>/', views.book_room, name='book'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('<int:pk>/', views.booking_detail, name='detail'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel'),
]
