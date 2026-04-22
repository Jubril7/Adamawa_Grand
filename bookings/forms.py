from django import forms
from django.utils import timezone
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('check_in_date', 'check_out_date', 'num_guests', 'special_requests')
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests or requirements?'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')
        today = timezone.now().date()

        if check_in and check_in < today:
            self.add_error('check_in_date', 'Check-in date cannot be in the past.')

        if check_in and check_out:
            if check_out <= check_in:
                self.add_error('check_out_date', 'Check-out date must be after check-in date.')

        return cleaned_data
