from django import forms
from .models import User, UserProfile
import re

ALLOWED_DOMAINS = [
     "lspu.edu.ph"   
    ]

ID_PATTERN = r"^\d{4}-\d{4}$"

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email', 'password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            local_part, domain = email.split('@')
        except ValueError:
            raise forms.ValidationError('Invalid email format')

        if domain not in ALLOWED_DOMAINS:
            raise forms.ValidationError('Use your institutional email')
        
        if not re.match(ID_PATTERN, local_part):
            raise forms.ValidationError('Invalid institution email format')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Account with this email already exists')

        return email
    
    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(email=email, password=password)
        return user
    
class AccountCompletion(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'profile_pic',
        ]