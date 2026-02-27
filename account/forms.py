from django import forms
from .models import User

ALLOWED_DOMAINS = [
     "lspu.edu.ph"   
    ]

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        domain = email.split('@')[-1].lower()

        if domain not in ALLOWED_DOMAINS:
            raise forms.ValidationError('Use your institutional email')
        
        return email