from django import forms

from .models import Company


class CreateCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'email', 'contact', 'photo', 'website', 'location']


class UpdateCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['email', 'contact', 'photo', 'website', 'location']
