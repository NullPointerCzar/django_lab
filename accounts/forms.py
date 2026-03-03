from django import forms
from .models import UserProfile
import re
from django.utils import timezone


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = "__all__"
        widgets = {
            'password': forms.PasswordInput,
            'dob': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mandatory fields
        for field in ['name', 'mobile', 'doctor_name', 'gender', 'dob',
                      'patient_id', 'email', 'file']:
            self.fields[field].required = True

    # ------------------------------------------------------------------ #
    # Field-level validators
    # ------------------------------------------------------------------ #

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) > 40:
            raise forms.ValidationError("Full name must be 40 characters or fewer.")
        return name

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '')
        # 10-digit numbers starting with 98/97/96  OR  landlines starting with 01 (9 digits)
        if not re.match(r'^(98|97|96)\d{8}$|^01\d{7}$', mobile):
            raise forms.ValidationError(
                "Enter a valid mobile number starting with 98, 97, or 96 (10 digits), "
                "or a landline starting with 01 (9 digits)."
            )
        return mobile

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if not re.match(r'^[A-Za-z]+\d+$', username):
            raise forms.ValidationError(
                "Username must start with letters followed by numbers (e.g. john123)."
            )
        return username

    def clean_appointment(self):
        appointment = self.cleaned_data.get('appointment')
        if appointment and appointment < timezone.now():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return appointment

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            ext = file.name.rsplit('.', 1)[-1].lower()
            allowed = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif']
            if ext not in allowed:
                raise forms.ValidationError(
                    f"Unsupported file type '.{ext}'. "
                    f"Allowed: {', '.join(allowed)}."
                )
            if file.size > 2 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 2 MB.")
        return file

    # ------------------------------------------------------------------ #
    # Cross-field validator (password complexity + confirmation)
    # ------------------------------------------------------------------ #

    def clean(self):
        data = super().clean()
        password = data.get('password', '')
        confirm = data.get('confirm_password', '')

        if password:
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            if not re.search(r'[a-z]', password):
                self.add_error('password', "Password must contain at least one lowercase letter.")
            if not re.search(r'[A-Z]', password):
                self.add_error('password', "Password must contain at least one uppercase letter.")
            if not re.search(r'\d', password):
                self.add_error('password', "Password must contain at least one digit.")
            if not re.search(r'[^A-Za-z0-9]', password):
                self.add_error('password', "Password must contain at least one special character.")

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match.")

        return data