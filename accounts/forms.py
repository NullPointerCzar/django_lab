from django import forms
from .models import UserProfile
import re
from datetime import datetime

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = "__all__"

    def clean(self):
        data = super().clean()

        # Mobile validation
        mobile = data.get("mobile")
        if mobile and not re.match(r'^(98|97|96)\d{8}$', mobile):
            raise forms.ValidationError("Invalid Mobile")

        # Username validation
        username = data.get("username")
        if username and not re.match(r'^[A-Za-z]+\d+$', username):
            raise forms.ValidationError("Invalid Username")

        # Password validation
        password = data.get("password")
        confirm = data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError("Password not match")

        if password and len(password) < 8:
            raise forms.ValidationError("Password too short")

        # Appointment date validation
        appointment = data.get("appointment")
        if appointment and appointment < datetime.now():
            raise forms.ValidationError("Past date not allowed")

        # File validation
        file = data.get("file")
        if file:
            ext = file.name.split('.')[-1].lower()
            allowed = ['pdf','doc','docx','ppt','pptx','jpg','jpeg','png','gif']
            if ext not in allowed:
                raise forms.ValidationError("Invalid file type")

            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File too large")

        return data