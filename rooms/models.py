from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='rooms')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveSmallIntegerField(default=2)
    description = models.TextField()
    amenities = models.TextField(
        help_text='Comma-separated list: e.g. WiFi, AC, TV, Mini Bar',
        blank=True
    )
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    floor = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['room_number']

    def __str__(self):
        return f'Room {self.room_number} — {self.room_type}'

    def get_amenities_list(self):
        return [a.strip() for a in self.amenities.split(',') if a.strip()]
