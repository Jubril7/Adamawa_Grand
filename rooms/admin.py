from django.contrib import admin
from .models import Room, RoomType


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'capacity', 'floor', 'is_available')
    list_filter = ('room_type', 'is_available', 'floor')
    list_editable = ('is_available', 'price_per_night')
    search_fields = ('room_number', 'description')
