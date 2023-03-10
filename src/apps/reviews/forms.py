from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['comment', 'rating']

        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control shadow px-2',
                    'rows': 6
                }
            ),
            'rating': forms.RadioSelect
        }
