from django.shortcuts import render, redirect
from django.contrib import messages
from rooms.models import Room, RoomType
from .models import HeroSlide
from .forms import ContactForm


def home(request):
    slides = HeroSlide.objects.filter(is_active=True)
    featured_rooms = Room.objects.filter(is_available=True).select_related('room_type')[:6]
    context = {
        'slides': slides,
        'featured_rooms': featured_rooms,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Thank you for your message. We will get back to you shortly.')
        return redirect('pages:contact')
    return render(request, 'pages/contact.html', {'form': form})
