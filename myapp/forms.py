import re
from django import forms
from django.db.models import Q
from .models import User

class SendOtpForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['name','email','mobile_number']
    
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if not re.match(r'^\d{10}$', mobile_number):
            raise forms.ValidationError('Mobile number must be a 10-digit ')
        return mobile_number

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile_number = cleaned_data.get('mobile_number')

        if User.objects.filter(Q(email=email) | Q(mobile_number=mobile_number)).exists():
            raise forms.ValidationError('A user with that email or mobile number already exists.')
