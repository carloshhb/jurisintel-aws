from django import forms
from .models import Tags


class CardForm(forms.Form):
    tag = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget=forms.widgets.CheckboxSelectMultiple()
    )
