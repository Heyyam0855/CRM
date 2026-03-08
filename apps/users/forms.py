"""Users App — Forms"""
from django import forms
from django.utils import timezone

from .models import User, StudentProfile, RegistrationRequest


class CourseRegistrationForm(forms.ModelForm):
    """Tələbə dərs qeydiyyat formu (Google Form tipli)."""

    LESSONS_PER_WEEK_CHOICES = [
        (1, '1 dərs / həftə'),
        (2, '2 dərs / həftə'),
        (3, '3 dərs / həftə'),
        (4, '4 dərs / həftə'),
        (5, '5 dərs / həftə'),
    ]

    lessons_per_week = forms.TypedChoiceField(
        choices=LESSONS_PER_WEEK_CHOICES,
        coerce=int,
        initial=2,
        widget=forms.RadioSelect(),
        label='Həftəlik dərs sayı',
    )

    class Meta:
        model = RegistrationRequest
        fields = [
            'full_name', 'email', 'phone', 'course_package',
            'other_course', 'lessons_per_week', 'payment_receipt',
            'preferred_start_date', 'github_profile_url',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ad və soyadınızı daxil edin',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+994501234567',
            }),
            'course_package': forms.RadioSelect(),
            'other_course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digər dərs paketinin adını yazın',
            }),
            'payment_receipt': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Qısa qeyd yazın',
            }),
            'preferred_start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'github_profile_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username',
            }),
        }
        labels = {
            'full_name': 'Ad Soyad',
            'email': 'Email',
            'phone': 'Telefon (Whatsapp)',
            'course_package': 'Hansı dərs paketi üzrə dərs almaq istəyirsiniz?',
            'other_course': 'Digər dərs paketi',
            'payment_receipt': 'Ödəmə məlumatı',
            'preferred_start_date': (
                'Hansı tarixdən başlamaq istəyirsiniz?'
            ),
            'github_profile_url': 'GitHub profil linki',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if RegistrationRequest.objects.filter(
            email=email,
            status=RegistrationRequest.Status.PENDING,
        ).exists():
            raise forms.ValidationError(
                'Bu email ilə artıq gözləmədə olan müraciət var.'
            )
        return email

    def clean_preferred_start_date(self):
        date = self.cleaned_data['preferred_start_date']
        if date and date < timezone.now().date():
            raise forms.ValidationError('Tarix keçmişdə ola bilməz.')
        return date

    def clean(self):
        cleaned_data = super().clean()
        package = cleaned_data.get('course_package')
        other = cleaned_data.get('other_course', '').strip()
        if package == RegistrationRequest.CoursePackage.OTHER and not other:
            self.add_error(
                'other_course',
                '"Digər" seçdiyiniz üçün dərs paketinin adını yazmalısınız.'
            )
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
