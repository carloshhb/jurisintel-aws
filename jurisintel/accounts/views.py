# Custom imports.
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from conteudo.views import retrieve_themes
from conteudo.forms import UserTema
from conteudo.models import Tema
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import pytz

from .forms import *
from .models import *


# Views
def index(request):
    return render(request, 'conteudo/home.html', {})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('home'))


def registro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('conteudo:home'))

    registered = False

    if request.method == 'POST':
        # It appears as one form to the user on the .html page
        user_form = RegisterForm(data=request.POST)

        if user_form.is_valid():

            # Save User Form to Database
            # user = user_form.save()
            # Remover o código abaixo quando for retirar a liberação gratuita de uso
            # ========================================
            user = user_form.save(commit=False)
            user.situacao_adesao = 'Ativo'
            user.save()
            # ========================================
            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            registered = True

            usuario = '%s %s' % (request.POST['first_name'], request.POST['last_name'])
            subject = 'Novo cadastro do usuário %s' % usuario
            to = ['assinaturas@jurisintel.com.br']
            from_email = request.POST['email']
            context = {
                'email': '%s' % from_email,
                'usuario': '%s' % usuario,
                'estado': '%s' % request.POST['estado_atuacao'],
                'area': '%s' % request.POST['area_atuacao'],
                'advogados': '%s' % request.POST['advogados_atuacao'],
                'processos': '%s' % request.POST['processos_ativos'],
            }
            mensagem = render_to_string('accounts/registration/marketing_email.html', context=context)
            send_mail(subject, mensagem, from_email, to, html_message=mensagem)

            return HttpResponseRedirect(reverse('accounts:user_login'))

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = RegisterForm()
    termos = settings.TERMOS_DE_USO
    pprivacidade = settings.POLITICA_PRIVACIDADE
    return render(request, 'accounts/registro.html', {'user_form':user_form, 'registered':registered, 'termos': termos,
                                                      'pprivacidade': pprivacidade})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('conteudo:home'))

    error_msg = False

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('conteudo:home'))
            else:
                return HttpResponse("Sua conta não está ativa.")
        else:
            error_msg = 'Credenciais inválidas.'
    else:
        login_form = LoginForm()

    return render(request, 'accounts/login.html', {'login_form': login_form, 'error_msg': error_msg})


def reset_password(request):
    return False


@method_decorator(login_required, name='dispatch')
class PerfilView(TemplateView):

    def get(self, request, *args, **kwargs):

        email = request.user.email
        user = User.objects.get(email__iexact=email)
        perfil_form = PerfilForm(instance=user)
        profile_form = ProfileForm(user=request.user)
        user_temas, all_temas = retrieve_themes(request)

        ut = UserTema(mode=True, user=request.user)
        at = UserTema(mode=None, user=request.user, prefix='avb')
        # try:
        #     lista_usuarios_por_escritorio = User.objects.filter(group_law_firm__id=request.user.group_law_firm.id)
        #     qtd_usuarios_por_escritorio = lista_usuarios_por_escritorio.count()
        #
        #     lista_processos_escritorio = Case.objects.filter(firm__exact=request.user.group_law_firm)
        #     qtd_processos_escritorio = lista_processos_escritorio.count()
        #
        #     lista_arquivos_escritorio = Files.objects.filter(processo__firm__exact=request.user.group_law_firm)
        #     qtd_arquivos_escritorio = lista_arquivos_escritorio.count()
        # except Exception as error:
        #     qtd_arquivos_escritorio, qtd_usuarios_por_escritorio, qtd_processos_escritorio = 0, 0, 0

        user_name = request.user.full_name
        context = {
            'user_name': user_name,
            'user_email': request.user.email,
            'formulario_usuario': perfil_form,
            'profile_form': profile_form,
            'temas': user_temas,
            'ut': ut,
            'at': at,
            # 'quant_users_firm': qtd_usuarios_por_escritorio,
            # 'quant_proc_firm': qtd_processos_escritorio,
            # 'quant_files_firm': qtd_arquivos_escritorio,
        }

        return render(request, 'accounts/perfil.html', context)

    def post(self, request, **kwargs):

        perfil_form = PerfilForm(request.POST, instance=request.user)

        if perfil_form.is_valid():
            perfil_form.save()
        else:
            perfil_form = PerfilForm(instance=request.user)

        profile_form = ProfileForm(user=request.user)
        user_name = request.user.full_name
        context = {
            'user_name': user_name,
            'user_email': request.user.email,
            'formulario_usuario': perfil_form,
            'profile_form': profile_form,
        }

        return render(request, 'accounts/perfil.html', context=context)


class AssinaturasView(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            plano_trial = PlanGroup.objects.get(usuario=request.user)
            if plano_trial.trial_status:
                trial = True
                d1 = plano_trial.end_date.strftime('%d/%m/%Y %H:%S')
                tipo_plano = plano_trial.plan.tipo
            else:
                trial = False
                d1 = ''
                tipo_plano = ''

        except Exception:
            trial = False
            d1 = ''
            tipo_plano = ''

        if trial:
            status = 'Período de Teste'
        else:
            status = 'Ativo'

        user_name = request.user.full_name
        context = {
            'trial': trial,
            'data_trial': d1,
            'plan_type': tipo_plano,
            'status': status,
            'user_name': user_name,
        }
        return render(request, 'accounts/profile_plans.html', context)


class EscritorioView(TemplateView):

    def get(self, request, *args, **kwargs):

        try:
            firm = request.user.group_law_firm
            form = EscritorioForm(instance=firm)
            if firm is not None:
                has_firm = True
            else:
                has_firm = False
        except Exception as error:
            form = EscritorioForm()
            has_firm = False

        user_name = request.user.full_name
        context = {
            'form': form,
            'user_name': user_name,
            'has_firm': has_firm,
        }

        return render(request, 'accounts/firm_view.html', context)

    def post(self, request, *args, **kwargs):

        form = EscritorioForm(request.POST, instance=request.user)
        data = dict()

        if form.is_valid():

            escritorio = request.user.group_law_firm

            if escritorio is None:
                data['valid'] = True
                firm = LawFirm.objects.create(law_firm=request.POST['law_firm'],
                                              law_firm_branch=request.POST['law_firm_branch'])
                user = request.user
                user.group_law_firm = firm
                user.save()
            else:
                data['valid'] = False

        return JsonResponse(data)


class RegistroTrial(TemplateView):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('conteudo:home'))

        user_form = TrialForm()
        termos = settings.TERMOS_DE_USO
        pprivacidade = settings.POLITICA_PRIVACIDADE

        return render(request, 'accounts/registro_trial.html', {'user_form': user_form, 'termos': termos,
                                                                'pprivacidade': pprivacidade})

    def post(self, request, *args, **kwargs):
        user_form = TrialForm(data=request.POST)
        plan_type = request.POST['trial']

        if plan_type == 'basic':
            plan_exists = True

        elif plan_type == 'premium':
            plan_exists = True

        else:
            msg = 'Erro ao selecionar plano.'
            plan_exists = False

        if plan_exists:
            if user_form.is_valid():
                # Save User Form to Database
                # user = user_form.save()
                # Remover o código abaixo quando for retirar a liberação gratuita de uso
                # ========================================
                user = user_form.save(commit=False)
                user.situacao_adesao = 'Ativo'
                user.save()
                # ========================================
                # Hash the password
                user.set_password(user.password)

                # Update with Hashed password
                user.save()

                plano = Planos.objects.get(tipo__iexact=plan_type)

                data1 = datetime.datetime.now(tz=pytz.UTC)
                data2 = data1 + datetime.timedelta(days=7)

                PlanGroup.objects.create(usuario=user, plan=plano, trial_status=True,
                                         status_assinatura=False, end_date=data2)

                # data1 = datetime.datetime.now()
                # data2 = data1 + datetime.timedelta(days=7)
                #
                # d1 = dateutil.parser.parse(data1.strftime('%m/%d/%Y'))
                # d2 = dateutil.parser.parse(data2.strftime('%m/%d/%Y'))

                # usuario = '%s %s' % (request.POST['first_name'], request.POST['last_name'])
                # subject = 'Novo cadastro do usuário %s' % usuario
                # to = ['assinaturas@jurisintel.com.br']
                # from_email = request.POST['email']
                # context = {
                #     'email': '%s' % from_email,
                #     'usuario': '%s' % usuario,
                # }
                # mensagem = render_to_string('accounts/registration/marketing_email.html', context=context)
                # send_mail(subject, mensagem, from_email, to, html_message=mensagem)

                return HttpResponseRedirect(reverse('accounts:user_login'))
            else:
                user_form = TrialForm()
                return render(request, 'accounts/registro_trial.html',
                              {'plan_exists': plan_exists, 'user_form': user_form})
        else:
            return render(request, 'accounts/registro_trial.html', {'plan_exists': plan_exists, 'user_form': user_form})


def change_password(request):
    data = dict()
    if request.POST:
        form = ProfileForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            data['is_valid'] = True
        else:
            data['is_valid'] = False
    else:
        form = ProfileForm(request.user)

    data['html_response'] = render_to_string('includes/profile_form.html', {'form': form}, request=request)
    return JsonResponse(data)


def add_temas_observe(request):
    data = dict()
    if request.POST:
        for tema_id in request.POST['titulo_tema']:
            tema = Tema.objects.get(pk=tema_id)
            try:
                tema.usuarios.objects.filter(usuarios=request.user)
            except Exception as error:
                tema.usuarios.add(request.user)
        data['is_valid'] = True
    return JsonResponse(data)
