from django import forms
from .models import *

from django import forms
from ckeditor.widgets import CKEditorWidget


class CustomCKEditorWidget(CKEditorWidget):
    def use_required_attribute(self, initial):
        return False

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if not value:
            return None
        value = value.replace("<p>", "").replace("</p>", "").replace("&#39;", "’").replace("&rsquo;", "’").replace("&nbsp;", "").replace("<br />", "")  # noqa
        return value


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

    image2 = forms.ImageField(
        widget=forms.FileInput()
    )

    image3 = forms.ImageField(
        widget=forms.FileInput()
    )

    image4 = forms.ImageField(
        widget=forms.FileInput()
    )

    image5 = forms.ImageField(
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


class NotificationForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ))
    image = forms.ImageField(
        widget=forms.FileInput()
    )
    image2 = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )

    image3 = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )

    image4 = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )

    image5 = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )

    class Meta:
        model = Notification
        fields = "__all__"
