from django.shortcuts import render, get_object_or_404
from .models import Room, RoomType


def room_list(request):
    rooms = Room.objects.filter(is_available=True).select_related('room_type')
    room_types = RoomType.objects.all()

    room_type_filter = request.GET.get('type')
    capacity_filter = request.GET.get('capacity')
    max_price = request.GET.get('max_price')

    if room_type_filter:
        rooms = rooms.filter(room_type__name__iexact=room_type_filter)
    if capacity_filter:
        rooms = rooms.filter(capacity__gte=capacity_filter)
    if max_price:
        rooms = rooms.filter(price_per_night__lte=max_price)

    context = {
        'rooms': rooms,
        'room_types': room_types,
        'applied_filters': {
            'type': room_type_filter,
            'capacity': capacity_filter,
            'max_price': max_price,
        },
    }
    return render(request, 'rooms/list.html', context)


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/detail.html', {'room': room})
