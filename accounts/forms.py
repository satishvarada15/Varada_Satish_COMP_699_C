from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, MotherProfile, VolunteerProfile


class MotherRegisterForm(UserCreationForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    risk_level = forms.ChoiceField(
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
    )
    location = forms.CharField(max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'due_date', 'risk_level', 'location'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'mother'

        if commit:
            user.save()
            MotherProfile.objects.create(
                user=user,
                due_date=self.cleaned_data.get('due_date'),
                risk_level=self.cleaned_data.get('risk_level'),
                location=self.cleaned_data.get('location'),
            )
        return user


class VolunteerRegisterForm(UserCreationForm):
    skills = forms.CharField(max_length=255, required=False)
    certifications = forms.CharField(max_length=255, required=False)
    service_limit = forms.IntegerField(initial=5)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'skills', 'certifications', 'service_limit'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'volunteer'

        if commit:
            user.save()
            VolunteerProfile.objects.create(
                user=user,
                skills=self.cleaned_data.get('skills'),
                certifications=self.cleaned_data.get('certifications'),
                service_limit=self.cleaned_data.get('service_limit')
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
