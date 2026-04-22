from django.db import models
from django.conf import settings
from rooms.models import Room
from decimal import Decimal


class Booking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.PositiveSmallIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Booking #{self.pk} — {self.user} | Room {self.room.room_number}'

    @property
    def num_nights(self):
        delta = self.check_out_date - self.check_in_date
        return delta.days

    def calculate_total(self):
        return self.room.price_per_night * self.num_nights

    def save(self, *args, **kwargs):
        if self.check_in_date and self.check_out_date:
            self.total_price = self.calculate_total()
        super().save(*args, **kwargs)

    def can_cancel(self):
        return self.status in (self.STATUS_PENDING, self.STATUS_APPROVED)
