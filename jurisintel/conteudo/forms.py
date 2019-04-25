from django import forms
from django.forms import formset_factory
from .models import Tags, Case


class CardForm(forms.Form):
    tag = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget=forms.widgets.CheckboxSelectMultiple()
    )


class UpdateCaseForm(forms.ModelForm):

    titulo = forms.CharField(label='Título', widget=forms.TextInput(attrs={'class': 'form-control'}))
    resumo = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))

    class Meta:
        model = Case
        fields = ['titulo', 'resumo']


class TagForm(forms.Form):

    tag = forms.CharField(label='Tags', widget=forms.TextInput(attrs={'class': 'form-control'}))


TagFormset = formset_factory(TagForm, extra=1)
