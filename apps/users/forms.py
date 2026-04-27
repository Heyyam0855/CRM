"""Users App — Forms"""
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import User, StudentProfile, RegistrationRequest


class CourseRegistrationForm(forms.ModelForm):
    """Tələbə dərs qeydiyyat formu (Google Form tipli)."""

    LESSONS_PER_WEEK_CHOICES = [
        (1, _('1 dərs / həftə')),
        (2, _('2 dərs / həftə')),
        (3, _('3 dərs / həftə')),
        (4, _('4 dərs / həftə')),
        (5, _('5 dərs / həftə')),
    ]

    lessons_per_week = forms.TypedChoiceField(
        choices=LESSONS_PER_WEEK_CHOICES,
        coerce=int,
        initial=2,
        widget=forms.RadioSelect(),
        label=_('Ħəftəlik dərs sayı'),
    )

    PAYMENT_METHOD_CHOICES = [
        ('epoint', _('Online ödəniş (kart ilə)')),
        ('bank_transfer', _('Bank köçürməsi')),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        initial='epoint',
        widget=forms.RadioSelect(),
        label=_('Ödəniş üslulu'),
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
                'class': 'form-input',
                'placeholder': 'Ad və soyadınızı daxil edin',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+994501234567',
            }),
            'course_package': forms.RadioSelect(),
            'other_course': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Digər dərs paketinin adını yazın',
            }),
            'payment_receipt': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Qısa qeyd yazın',
            }),
            'preferred_start_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'github_profile_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://github.com/username',
            }),
        }
        labels = {
            'full_name': _('Ad Soyad'),
            'email': _('Email'),
            'phone': _('Telefon (Whatsapp)'),
            'course_package': _('Hansı dərs paketi üzrə dərs almaq istəyirsiniz?'),
            'other_course': _('Digər dərs paketi'),
            'payment_receipt': _('Ödəmə məlumatı'),
            'preferred_start_date': _('Hansı tarixdən başlamaq istəyirsiniz?'),
            'github_profile_url': _('GitHub profil linki'),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if RegistrationRequest.objects.filter(
            email=email,
            status=RegistrationRequest.Status.PENDING,
        ).exists():
            raise forms.ValidationError(
                _('Bu email ilə artıq gözləmədə olan müraciət var.')
            )
        return email

    def clean_preferred_start_date(self):
        date = self.cleaned_data['preferred_start_date']
        if date and date < timezone.now().date():
            raise forms.ValidationError(_('Tarix keçmişdə ola bilməz.'))
        return date

    def clean(self):
        cleaned_data = super().clean()
        package = cleaned_data.get('course_package')
        other = cleaned_data.get('other_course', '').strip()
        if package == RegistrationRequest.CoursePackage.OTHER and not other:
            self.add_error(
                'other_course',
                _('"Digər" seçdiyiniz üçün dərs paketinin adını yazmalısınız.')
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
            'github_username': _('GitHub istifadəçi adı'),
            'timezone': _('Vaxt zonası'),
            'education_level': _('Təhsil səviyyəsi'),
            'goals': _('Öyrənmə hədəflərim'),
        }
