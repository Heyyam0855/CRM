"""Users App — Forms"""
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, StudentProfile


class StudentRegistrationForm(forms.Form):
    """Tələbə qeydiyyat formu."""

    first_name = forms.CharField(
        max_length=100,
        label='Ad',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız'})
    )
    last_name = forms.CharField(
        max_length=100,
        label='Soyad',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadınız'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    phone = forms.CharField(
        max_length=20,
        label='Telefon',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+994501234567'})
    )
    password1 = forms.CharField(
        label='Şifrə',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Şifrəni təkrar daxil edin',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    payment_model = forms.ChoiceField(
        choices=StudentProfile.PaymentModel.choices,
        label='Ödəniş modeli',
        widget=forms.RadioSelect()
    )
    lessons_per_week = forms.IntegerField(
        min_value=1,
        max_value=7,
        initial=2,
        label='Həftəlik dərs sayı',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        label='Qeyd',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Əlavə məlumat, suallarınız və ya xüsusi istəklərinizi bura yazın...'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email artıq qeydiyyatdan keçib.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Şifrələr uyğun gəlmir.')
        return cleaned_data


class StudentProfileUpdateForm(forms.ModelForm):
    """Tələbə profil yeniləmə formu."""

    class Meta:
        model = StudentProfile
        fields = ['github_username', 'timezone', 'education_level', 'goals']
        widgets = {
            'github_username': forms.TextInput(attrs={'class': 'form-control'}),
            'timezone': forms.Select(attrs={'class': 'form-select'}),
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'github_username': 'GitHub istifadəçi adı',
            'timezone': 'Vaxt zonası',
            'education_level': 'Təhsil səviyyəsi',
            'goals': 'Öyrənmə hədəflərim',
        }
