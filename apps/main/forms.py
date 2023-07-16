from django import forms
from .models import *


class SaleForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ))

    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ))
    image = forms.ImageField(
      widget=forms.FileInput()
    )

    class Meta:
        model = Sale
        fields = "__all__"


class NewsForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ))

    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ))
    image = forms.ImageField(
      widget=forms.FileInput()
    )

    min_age = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    max_age = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    for_gender = forms.ChoiceField(
        choices=News.GENDER,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = News
        fields = "__all__"

