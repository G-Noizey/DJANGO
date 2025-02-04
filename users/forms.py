from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'name', 'surname', 'control_number',
            'age', 'tel', 'password1', 'password2'
        ]

        common_attrs = {'class': 'form-control', 'required': True}

        widgets = {
            'email': forms.EmailInput(attrs={
                **common_attrs,
                'placeholder': 'Correo electrónico',
                'pattern': r'^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$',
                'title': 'Debe ser un correo de UTEZ (ejemplo: usuario@utez.edu.mx).',
            }),
            'name': forms.TextInput(attrs={
                **common_attrs,
                'placeholder': 'Nombre',
                'minlength': 2,
                'maxlength': 50,
                'pattern': r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
                'title': 'Solo letras y espacios (2-50 caracteres).',
            }),
            'surname': forms.TextInput(attrs={
                **common_attrs,
                'placeholder': 'Apellido',
                'minlength': 2,
                'maxlength': 50,
                'pattern': r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
                'title': 'Solo letras y espacios (2-50 caracteres).',
            }),
            'control_number': forms.TextInput(attrs={
                **common_attrs,
                'placeholder': 'Número de control',
                'minlength': 10,
                'maxlength': 10,
                'pattern': r'^\d{5}[a-z]{2}\d{3}$',
                'title': 'Debe seguir el formato: 5 dígitos, 2 letras minúsculas y 3 dígitos.',
            }),
            'age': forms.NumberInput(attrs={
                **common_attrs,
                'placeholder': 'Edad',
                'min': 18,
                'max': 99,
                'title': 'Debe estar entre 18 y 99 años.',
            }),
            'tel': forms.TextInput(attrs={
                **common_attrs,
                'placeholder': 'Teléfono',
                'pattern': r'^\d{10}$',
                'title': 'Debe ser un número de 10 dígitos.',
            }),
            'password1': forms.PasswordInput(attrs={
                **common_attrs,
                'placeholder': 'Contraseña',
                'minlength': 8,
                'title': 'Debe tener al menos 8 caracteres, una mayúscula, un número y un carácter especial.',
            }),
            'password2': forms.PasswordInput(attrs={
                **common_attrs,
                'placeholder': 'Confirmar contraseña',
                'minlength': 8,
                'title': 'Debe coincidir con la contraseña ingresada.',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@utez.edu.mx'):
            raise ValidationError("El correo electrónico debe ser de UTEZ (ejemplo: usuario@utez.edu.mx).")
        return email

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if not re.fullmatch(r'\d{10}', tel):
            raise ValidationError("El número de teléfono debe tener exactamente 10 dígitos.")
        return tel

    def clean_control_number(self):
        control_number = self.cleaned_data.get('control_number')
        if not re.fullmatch(r'^\d{5}[a-z]{2}\d{3}$', control_number):
            raise ValidationError("El número de control debe seguir el formato: 5 dígitos, 2 letras minúsculas y 3 dígitos.")
        return control_number

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None or not (18 <= age <= 99):
            raise ValidationError("La edad debe estar entre 18 y 99 años.")
        return age

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'[0-9]', password1):
            raise ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise ValidationError("La contraseña debe contener al menos un carácter especial.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError({'password2': "Las contraseñas no coinciden."})

        return cleaned_data


class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo electrónico',
        'required': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
        'required': True,
    }))
