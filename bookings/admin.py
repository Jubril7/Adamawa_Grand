from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in_date', 'check_out_date', 'num_nights', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'check_in_date', 'created_at')
    list_editable = ('status',)
    search_fields = ('user__username', 'user__email', 'room__room_number')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

    def num_nights(self, obj):
        return obj.num_nights
    num_nights.short_description = 'Nights'
