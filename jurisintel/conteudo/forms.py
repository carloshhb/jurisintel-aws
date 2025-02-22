from django import forms
from django.forms import formset_factory
from .models import Case, Ementa, Tags, Tema
from accounts.models import User


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


class TagsForm(forms.Form):

    tag = forms.CharField(label='Tags', widget=forms.TextInput(attrs={'class': 'form-control'}))


class TemaForm(forms.ModelForm):
    titulo_tema = forms.CharField(label='Título do Tema', widget=forms.TextInput(attrs={'class': 'form-control'}))
    descricao_tema = forms.CharField(
        label='Descrição/Resumo',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '8'}
        )
    )
    ementas = forms.ModelMultipleChoiceField(
        queryset=Ementa.objects.all(),
        widget=forms.widgets.CheckboxSelectMultiple()
    )

    class Meta:
        model = Tema
        fields = ['titulo_tema', 'descricao_tema', 'ementas']


class EditTemaForm(forms.ModelForm):
    titulo_tema = forms.ModelChoiceField(queryset=Tema.objects.all(),
                                         to_field_name=None,
                                         widget=forms.Select(attrs={'class': 'form-control edit-select'})
                                         )

    class Meta:
        model = Tema
        fields = ['titulo_tema']


class UserTema(forms.ModelForm):
    titulo_tema = forms.ModelMultipleChoiceField(queryset=Tema.objects.none(), required=False, widget=forms.SelectMultiple(
        attrs={'class': 'form-control'}
    ))

    class Meta:
        model = Tema
        fields = ['titulo_tema']

    def __init__(self, mode, user, *args, **kwargs):
        super(UserTema, self).__init__(*args, **kwargs)
        if mode is None:
            self.fields['titulo_tema'].queryset = Tema.objects.all().exclude(usuarios=user)
            self.fields['titulo_tema'].label = 'Temas disponíveis'
        else:
            self.fields['titulo_tema'].queryset = Tema.objects.filter(usuarios=user)
            self.fields['titulo_tema'].label = 'Temas acompanhados'


class CaseAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(label="Usuário", queryset=User.objects.all(), required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    titulo = forms.CharField(label="Título", widget=forms.TextInput(attrs={'class': 'form-control'}))
    resumo = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '8'}))
    docs = forms.FileField(label='Documentos', widget=forms.FileInput(attrs={'class': 'form-control', 'multiple': True}))

    class Meta:
        model = Case
        fields = ['user', 'titulo', 'resumo', 'docs']


TagsFormset = formset_factory(TagsForm, extra=1)
