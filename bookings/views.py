from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rooms.models import Room
from .models import Booking
from .forms import BookingForm


@login_required
def book_room(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk, is_available=True)
    form = BookingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        num_guests = form.cleaned_data['num_guests']
        if num_guests > room.capacity:
            messages.error(request, f'This room accommodates a maximum of {room.capacity} guests.')
            return render(request, 'bookings/book.html', {'form': form, 'room': room})

        booking = form.save(commit=False)
        booking.user = request.user
        booking.room = room
        booking.save()
        messages.success(request, f'Booking request submitted! Your booking #{booking.pk} is pending approval.')
        return redirect('bookings:my_bookings')

    return render(request, 'bookings/book.html', {'form': form, 'room': room})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room', 'room__room_type')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if not booking.can_cancel():
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:detail', pk=pk)
    if request.method == 'POST':
        booking.status = Booking.STATUS_CANCELLED
        booking.save()
        messages.success(request, f'Booking #{booking.pk} has been cancelled.')
        return redirect('bookings:my_bookings')
    return render(request, 'bookings/cancel_confirm.html', {'booking': booking})
