import datetime

from django import forms

from .models import User, LawFirm

choice_estado = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)

choice_area = (
    ('Administrativo', 'Administrativo'),
    ('Ambiental', 'Ambiental'),
    ('Civil Contratos', 'Civil Contratos'),
    ('Civil Família', 'Civil Família'),
    ('Civil Real', 'Civil Real'),
    ('Civil Outro', 'Civil Outro'),
    ('Consumidor', 'Consumidor'),
    ('Eleitoral', 'Eleitoral'),
    ('Empresarial', 'Empresarial'),
    ('Imobiliário', 'Imobiliário'),
    ('Penal', 'Penal'),
    ('Previdenciário', 'Previdenciário'),
    ('Trabalho', 'Trabalho'),
    ('Tributário', 'Tributário'),
    ('Outra', 'Outra')
)
choice_advogados = (
    ('Solo', 'Atuo sozinho'),
    ('2-3', 'de 2 a 3'),
    ('4-7', 'de 4 a 7'),
    ('8-12', 'de 8 a 12'),
    ('13-20', 'de 13 a 20'),
    ('21-30', 'de 21 a 30'),
    ('31-40', 'de 31 a 40'),
    ('41-50', 'de 41 a 50'),
    ('51-100', 'de 51 a 100'),
    ('+100', 'Mais de 100'),

)
choice_processos = (
    ('menos de 100', 'menos de 100'),
    ('entre 100 e 500', 'entre 100 e 500'),
    ('mais de 500 e menos de 1.000', 'mais de 500 e menos de 1.000'),
    ('entre 1.000 e 1.500', 'entre 1.000 e 1.500'),
    ('mais de 1.500 e menos de 2.000', 'mais de 1.500 e menos de 2.000'),
    ('entre 2.000 e 3.000', 'entre 2.000 e 3.000'),
    ('mais de 3.000 e menos de 4.000', 'mais de 3.000 e menos de 4.000'),
    ('entre 4.000 e 5.000', 'entre 4.000 e 5.000'),
    ('mais de 5.000 e menos de 6.000', 'mais de 5.000 e menos de 6.000'),
    ('entre 6.000 e 7.000', 'entre 6.000 e 7.000'),
    ('mais de 7.000 e menos de 8.000', 'mais de 7.000 e menos de 8.000'),
    ('entre 8.000 e 9.000', 'entre 8.000 e 9.000'),
    ('mais de 9.000 e menos de 10.000', 'mais de 9.000 e menos de 10.000'),
    ('10.000 ou mais', '10.000 ou mais'),
)


class RegisterForm(forms.ModelForm):

    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #Lista de anos para seletor de data
    initial = datetime.date(year=1990, month=1, day=1)
    hoje = datetime.date.today()
    anos = []
    for a in range(1900,hoje.year):
        anos.append(a)
    birthdate = forms.DateField(initial=initial, label='Data de Nascimento',
                                widget=forms.SelectDateWidget(years=anos,
                                                              attrs={'class': 'custom-select'}))
    
    estado_atuacao = forms.ChoiceField(
        label='Estado em que mais atua',
        choices=choice_estado,
        help_text='Escolha aquele em que você atua com mais frequência.',
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    
    area_atuacao = forms.ChoiceField(
        label='Área de maior atuação',
        choices=choice_area,
        help_text='Escolha uma área do Direito em que você atua de forma preponderante.',
        widget=forms.Select(attrs={'class': 'form-control'}))
    
    advogados_atuacao = forms.ChoiceField(
        label='Advogados no escritório',
        choices=choice_advogados,
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    
    processos_ativos = forms.ChoiceField(
        label='Processos ativos que existem no escritório',
        choices=choice_processos,
        help_text='É apenas uma estimativa.',
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    
    class Meta():
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'birthdate',
         'estado_atuacao', 'area_atuacao', 'advogados_atuacao', 'processos_ativos']


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PerfilForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    hoje = datetime.date.today()
    anos = []
    for a in range(1900, hoje.year):
        anos.append(a)
    birthdate = forms.DateField(label='Data de Nascimento',
                                widget=forms.SelectDateWidget(years=anos, attrs={'class': 'custom-select'}))

    class Meta():
        model = User
        fields = ['email', 'first_name', 'last_name', 'birthdate']


class EscritorioForm(forms.ModelForm):
    law_firm = forms.CharField(label='Nome do Escritório', max_length=120, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    law_firm_branch = forms.CharField(label='Unidade do escritório', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta():
        model = LawFirm
        fields = ['law_firm', 'law_firm_branch']


planos = (
    ('basic', 'Básico'),
    ('premium', 'Premium'),
)


class TrialForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # Lista de anos para seletor de data
    initial = datetime.date(year=1990, month=1, day=1)
    hoje = datetime.date.today()
    anos = []
    for a in range(1900, hoje.year):
        anos.append(a)
    birthdate = forms.DateField(initial=initial, label='Data de Nascimento',
                                widget=forms.SelectDateWidget(years=anos,
                                                              attrs={'class': 'custom-select'}))
    trial = forms.ChoiceField(label='Plano', choices=planos, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta():
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'birthdate', 'trial']