import csv
import mimetypes
import os
import secrets
import tempfile
import unicodedata
import six
import docx2txt
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.db.models.query import QuerySet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pdf2image import convert_from_path
from wand.image import Image as wi

from accounts.models import User
from jurisintel.storage_backends import PublicMediaStorage, ThumbnailStorage
from .forms import CardForm, UpdateCaseForm, TagsFormset, TemaForm, EditTemaForm
from .models import Case, File, Tags, Thumbnail, Tema, Ementa
from .nlp.jurisintel_resumidor import resumidor as res
from .nlp.jurisintel_resumidor import resumidor_from_texto as resumo_texto
from .nlp.similar import similar_resumo, similar_tags
from .utils import get_documents_, get_case_tags, get_case_ementas, get_printable_size, get_documents_tema, \
    get_info_file, tesseract_extract, antiword_extract


# Create your views here.

# tipos de arquivos
DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
DOC = 'application/msword'
PDF = 'application/pdf'

def retrieve_cases(request):
    """
    Function to retrieve all cases from user or firm user is attached to.
    :param request: wsgi request.
    :return: parameters, tag_list, pages for pagination. Both lists.
    """
    parameters, tag_list = list(), list()
    pages = []
    page = request.GET.get('page', 1)
    try:
        users = User.objects.filter(escritorio__id=request.user.escritorio.pk)
        all_cases = QuerySet(model=Case)
        for user in users:
            all_cases = all_cases | Case.objects.filter(user=user).order_by('-created_at')
        paginator = Paginator(all_cases, 10)
        for case in paginator.object_list:
            try:
                if len(case.resumo) > 411:
                    resumo = '%s ...' % case.resumo[0:411]
                    fit = True
                else:
                    resumo = case.resumo
                    fit = False
            except Exception:
                resumo, fit = '', False
            param_dict = {
                'titulo': case.titulo,
                'resumo': resumo,
                'fit': fit,
                'possible_edit': True,
            }
            parameters.append([case.pk, param_dict])
            for tag in case.tags.all():
                tag_list.append([case.pk, [tag.__str__()]])

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

    except AttributeError:
        all_cases = Case.objects.filter(user=request.user).order_by('-created_at')
        paginator = Paginator(all_cases, 10)
        for case in paginator.object_list:
            try:
                if len(case.resumo) > 411:
                    resumo = '%s ...' % case.resumo[0:411]
                    fit = True
                else:
                    resumo = case.resumo
                    fit = False
            except Exception:
                resumo, fit = '', False
            param_dict = {
                'titulo': case.titulo,
                'resumo': resumo,
                'fit': fit,
                'possible_edit': True,
            }
            parameters.append([case.pk, param_dict])
            for tag in case.tags.all():
                tag_list.append([case.pk, [tag.__str__()]])

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

    except Exception as error:
        print(error)

    return parameters, tag_list, pages


def retrieve_themes(request):
    all_themes = Tema.objects.all()
    tema_user = all_themes.filter(usuarios=request.user)
    user_themes = list()
    for tema in tema_user:
        if len(tema.descricao_tema) > 411:
            resumo = '%s ...' % tema.descricao_tema[0:411]
            fit = True
        else:
            resumo = tema.descricao_tema
            fit = False
        param_dict = {
            'titulo': tema.titulo_tema,
            'resumo': resumo,
            'fit': fit,
            'possible_edit': False,
            'tema': True,
        }
        user_themes.append([tema.pk, param_dict])

    parameters = list()

    for tema in all_themes:
        param_dict = {
            'titulo': tema.titulo_tema,
        }
        parameters.append([tema.pk, param_dict])

    return user_themes, parameters


@login_required(login_url='user_login')
def home(request):
    if 's' in request.GET:
        search = request.GET['s']
        return filter_by_anything(request, search)

    if request.user.profile.allow_entrance:
        parameters, tag_list, pages = retrieve_cases(request)
        user_themes, all_themes = retrieve_themes(request)

        context = {
            'parameters': parameters,
            'tags': tag_list,
            'themes': user_themes,
            'pages': pages,
        }
        return render(request, 'conteudo/home.html', context)
    else:
        return HttpResponseRedirect(reverse('accounts:agendamento'))


def upload(request):

    data = dict()
    file_error = list()
    if request.POST:
        s3_file = PublicMediaStorage()
        s3_file.file_overwrite = False

        s3_thumb = ThumbnailStorage()
        s3_thumb.file_overwrite = False

        for file in request.FILES.getlist('files'):
            if not file.size > 5000000:
                try:
                    file_mimetype = mimetypes.guess_type(str(file))
                    if file_mimetype[0] == PDF:
                        pdf = wi(file=file, resolution=200)
                    arquivo = unicodedata.normalize('NFD', str(file)).encode('ASCII', 'ignore').decode('ASCII')
                    path = '%s/%s' % (str(request.user.pk), arquivo)
                    uploaded_file = s3_file.save(path, file)
                    save_file = File.objects.create(file=uploaded_file)
                except Exception as error:
                    print("erro 1: " + str(error))
                    data['error'] = str(error)
                else:
                    if save_file:
                        data['is_valid'] = True
                        data['file_id'] = save_file.pk
                    else:
                        data['is_valid'] = False

                    file_mimetype = mimetypes.guess_type(arquivo)
                    if file_mimetype[0] == PDF:
                        try:
                            thumbnail_image = pdf.convert("jpeg")
                            temp_image = tempfile.SpooledTemporaryFile()
                            pdf_name = str(arquivo).split('.pdf')
                            thumb_name = '%s.jpg' % pdf_name[0]

                            with thumbnail_image.sequence[0] as img:
                                page = wi(image=img)
                                page.width = 150
                                page.height = 200
                                page.strip()
                                page.save(file=temp_image)
                                img_file = s3_thumb.save(thumb_name, temp_image)
                                thumbnail = Thumbnail.objects.create(thumbnail=img_file)
                                save_file.thumbnail = thumbnail
                                save_file.save()
                        except Exception as error:
                            print("erro 2" + str(error))
                            data['error'] = str(error)
                    else:
                        save_file.thumbnail = None
            else:
                arquivo = unicodedata.normalize('NFD', str(file)).encode('ASCII', 'ignore').decode('ASCII')
                file_error.append([arquivo, get_printable_size(file.size)])

        data['file_error'] = file_error
        if len(data['file_error']) != 0:
            data['is_valid'] = False
        return JsonResponse(data)


def random_name(size):
    return secrets.token_hex(size)


def criar_resumo(arquivo, objeto):
    k = requests.get(arquivo.url, stream=True)
    file_mimetype = mimetypes.guess_type(k.url)

    # verificar o tipo do arquivo
    if file_mimetype[0] == PDF:
        # Nome do arquivo temporário
        temp_filename = '%s.pdf' % random_name(10)
        tmp_file = 'tmp/' + temp_filename
        with open(tmp_file, "wb") as fd:
            for chunk in k.iter_content(chunk_size=128):
                fd.write(chunk)

        try:
            # processar com pdfminer (slate3k)
            objeto.resumo = res(tmp_file)
            objeto.save()
        except Exception:
            # processar com tesseract
            temp_dir = tempfile.mkdtemp()
            base = os.path.join(temp_dir, 'conv')
            contents = []
            try:
                convert_from_path(tmp_file, fmt='jpeg', dpi=300, output_folder=temp_dir)
                for page in sorted(os.listdir(temp_dir)):
                    page_path = os.path.join(temp_dir, page)
                    page_content = tesseract_extract(page_path)
                    contents.append(page_content)
                resultado = six.b('').join(contents).decode()

                resumo = resumo_texto(resultado)
                if len(resumo) < 30:
                    objeto.resumo = resultado
                else:
                    objeto.resumo = resumo
                objeto.save()
            except Exception as error:
                print(error)

        # Remover o arquivo temporário
        os.remove(tmp_file)

    # processar arquivo docx
    elif file_mimetype[0] == DOCX:
        # Nome do arquivo temporário
        temp_filename = '%s.docx' % random_name(10)
        tmp_file = 'tmp/' + temp_filename
        with open(tmp_file, "wb") as fd:
            for chunk in k.iter_content(chunk_size=128):
                fd.write(chunk)

        conteudo = docx2txt.process(tmp_file)
        resumo = resumo_texto(conteudo)
        if len(resumo) < 30:
            objeto.resumo = conteudo
        else:
            objeto.resumo = resumo
        objeto.save()

        # Remover o arquivo temporário
        os.remove(tmp_file)

    # processar arquivo doc
    elif file_mimetype[0] == DOC:
        # Nome do arquivo temporário
        temp_filename = '%s.doc' % random_name(10)
        tmp_file = 'tmp/' + temp_filename
        with open(tmp_file, "wb") as fd:
            for chunk in k.iter_content(chunk_size=128):
                fd.write(chunk)

        resultado = antiword_extract(tmp_file)
        resumo = resumo_texto(resultado)
        if len(resumo) < 30:
            objeto.resumo = resultado
        else:
            objeto.resumo = resumo
        objeto.save()

        # Remover o arquivo temporário
        os.remove(tmp_file)


def file_upload(request):

    dados = list()
    form = CardForm()

    if request.POST:
        # Criar o caso antes, e se não confirmar na proxima tela, remover
        pre_case = Case.objects.create(user=request.user)
        indices, tag_list = list(), list()
        ids = request.POST['file-list-id'].split(';')
        for pk in ids:
            if pk is not '':
                file_object = get_object_or_404(File, pk=pk)

                criar_resumo(file_object.file, file_object)

                # TAGS COMPARISON
                # CREATE TAG LIST
                list_of_tags, index_list = list(), list()
                all_tags = Tags.objects.all()
                for t in all_tags:
                    list_of_tags.append(t.tag)
                    index_list.append(t.id)

                # CREATE TAG SIMILARITY
                tags_obj = similar_tags(file_object.resumo, list_of_tags)
                for s in tags_obj:
                    if s[1] > 0.18:
                        indices.append([s[1], list_of_tags[s[0]], index_list[s[0]]])
                # ORDER FOR SIMILARITY WITH TEXT
                indices.sort(key=lambda x: x[0], reverse=True)

                for x in indices:
                    tag_dict = {
                        'tag': x[1],
                    }
                    tag_list.append([x[2], tag_dict])

                # passa as strings para a view
                try:
                    thumb = str(file_object.thumbnail.thumbnail.url)
                except Exception:
                    thumb = 'docx'
                try:
                    file = str(file_object.file).split('/')[1]
                except Exception as error:
                    file = str(file_object.file)
                contexto = {
                    'arquivo': file,
                    'thumbnail': thumb,
                    'resumo': file_object.resumo,
                }
                dados.append([file_object.pk, contexto])

                pre_case.docs.add(file_object)

        context = {
            'dados': dados,
            'form': form,
            'pre_case_id': pre_case.pk,
            'tags_list': tag_list,
        }

        return render(request, 'conteudo/create_card.html', context)

    else:

        return HttpResponseRedirect(reverse('conteudo:home'))


def create(request):

    if request.POST:
        resumo = request.POST['descriptionAddCard']
        titulo = request.POST['tituloAddCard']

        pre_created_case = get_object_or_404(Case, pk=request.POST['case_id'])

        if pre_created_case:
            pre_created_case.titulo = titulo
            pre_created_case.resumo = resumo
            for tag in request.POST.getlist('tag'):
                t = Tags.objects.get(pk=tag)
                pre_created_case.tags.add(t)
            pre_created_case.save()

        return HttpResponseRedirect(reverse('conteudo:home'))


def open_case(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.user == case.user or request.user.escritorio == case.user.escritorio:

        documentos = get_documents_(case)
        tags = get_case_tags(case)

        try:
            tamanho_resumo = len(case.resumo)
            if tamanho_resumo > 730:
                resumo_fit = '%s ...' % case.resumo[0:730]
            else:
                resumo_fit = ''
        except Exception:
            resumo_fit = ''

        context = {
            'titulo': case.titulo,
            'resumo_fit': resumo_fit,
            'resumo': case.resumo,
            'documentos': documentos,
            'tags': tags,
            'pk': pk,
        }

        return render(request, 'conteudo/open_case.html', context)
    else:
        return HttpResponseRedirect(reverse('conteudo:home'))


def open_tema(request, pk):
    tema = get_object_or_404(Tema, pk=pk)
    ementas = get_case_ementas(tema)
    documentos = get_documents_tema(tema)
    # tags = get_case_tags(tema)

    context = {
        'titulo': tema.titulo_tema,
        'resumo': tema.descricao_tema,
        'documentos': documentos,
        'ementas': ementas,
        'pk': pk,
        # 'tags': tags,
    }

    return render(request, 'conteudo/open_tema.html', context)


def remover_arquivo(request, pk):
    if request.POST:
        data = dict()

        try:
            arquivo = File.objects.get(pk=pk)
            arquivo.delete()
            data['is_valid'] = True
        except Exception:
            data['is_valid'] = False

        case_pk = request.POST['case_id']
        case = Case.objects.get(pk=case_pk)
        documentos = get_documents_(case)
        context = {
            'documentos': documentos
        }
        data['is_valid'] = True
        data['html_docs_similares'] = render_to_string('conteudo/includes/similares_docs_list.html', context=context,
                                                       request=request)
        data['html_docs'] = render_to_string('conteudo/includes/docs_view.html', context=context, request=request)
        return JsonResponse(data)


def save_ementas(doc):
    with open(doc, encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]
    ementas_set = set()
    for x in data['ementa']:
        ementas_set.add(x)
    ementas_list = list(ementas_set)

    for k in ementas_list:
        Ementa.objects.create(orgao='CARF', texto=k)


def verify_similarities(request, pk):
    if request.POST:
        file_to_verify = File.objects.get(pk=request.POST['file'])
        resumo_referencia = file_to_verify.resumo
        if resumo_referencia is not None:

            try:
                users = User.objects.filter(escritorio__id=request.user.escritorio.pk)
                all_files = QuerySet(model=File)
                for user in users:
                    all_files = all_files | File.objects.filter(case__user=user).exclude(file=file_to_verify)
            except Exception:
                all_files = File.objects.filter(case__user=request.user).exclude(file=file_to_verify)

            filtered_list, filtered_list_ids = list(), list()

            for file in all_files:
                if file.resumo is None:
                    pass
                else:
                    if len(file.resumo) > 30:
                        filtered_list.append(str(file.resumo))
                        filtered_list_ids.append(file.pk)

            similares = similar_resumo(resumo_referencia, filtered_list)

            indices = list()

            for s in similares:
                indices.append([s[1], filtered_list[s[0]], filtered_list_ids[s[0]]])

            indices.sort(key=lambda x: x[0], reverse=True)

            similar_list = list()
            i = 0
            for k in indices:
                if i < len(indices) and i < 30:
                    f = File.objects.get(pk=k[2])
                    dados = get_info_file(f, k[0])
                    similar_list.append([f.pk, dados])
                    i += 1
                else:
                    break

            context = {'resultado': similar_list}
            data = {
                'html_resultado': render_to_string('conteudo/includes/similares_resultado.html', context=context, request=request)
            }

            return JsonResponse(data)
        else:
            context = {'error': 'erro'}
            data = {'html_resultado': render_to_string('conteudo/includes/similares_resultado.html', context=context, request=request)}

            return JsonResponse(data)

    else:
        case = get_object_or_404(Case, pk=pk)

        documentos = get_documents_(case)

        data = dict()
        context = {
            'documentos': documentos,
            'pk': pk,
        }
        data['html_similares'] = render_to_string(template_name='conteudo/includes/similares.html', context=context,
                                                  request=request)

        return JsonResponse(data)


def conteudo_juridico(request, pk):
    tema = get_object_or_404(Tema, pk=pk)
    ementas = get_case_ementas(tema)

    data = dict()
    context = {
        'pk': pk,
        'ementas': ementas,
    }
    data['html_precedents'] = render_to_string(template_name='conteudo/includes/precedents.html', context=context,
                                               request=request)

    return JsonResponse(data)


def precedents(request, pk):

    case = get_object_or_404(Case, pk=pk)

    ementas = get_case_ementas(case)

    data = dict()
    context = {
        'pk': pk,
        'ementas': ementas,
    }
    data['html_precedents'] = render_to_string(template_name='conteudo/includes/precedents.html', context=context,
                                               request=request)

    return JsonResponse(data)


def card_delete(request, pk):
    data = dict()
    try:
        case = Case.objects.get(pk=pk)
    except Exception as error:
        print(error)
    else:
        if request.method == 'POST':
            case.delete()
            data['form_is_valid'] = True

            parameters, tag_list, pages = retrieve_cases(request)

            update_context = {
                'parameters': parameters,
                'tags': tag_list,
            }
            data['html_response'] = render_to_string('conteudo/includes/cards.html', update_context)

        else:
            context = {'caso': case}
            data['html_form'] = render_to_string('conteudo/includes/card_delete.html', context, request=request)

        return JsonResponse(data)


def card_update(request, pk):
    caso = get_object_or_404(Case, pk=pk)

    if request.POST:
        form = UpdateCaseForm(request.POST, instance=caso)

    else:
        form = UpdateCaseForm(instance=caso)
    return save_(request, form, 'conteudo/includes/card_update.html')


def add_card_tags(request, pk):

    if request.POST:
        formset = TagsFormset(request.POST)

    else:
        formset = TagsFormset()
    return save_tag(request, formset, 'conteudo/includes/add_tags.html', pk)


def save_(request, form, template):

    data = dict()

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            data['form_is_valid'] = True

            parameters, tag_list, pages = retrieve_cases(request)

            update_context = {
                'parameters': parameters,
                'tags': tag_list,
            }
            data['html_response'] = render_to_string('conteudo/includes/cards.html', update_context)

        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template, context, request=request)
    return JsonResponse(data)


def save_tag(request, formset, template, pk):

    data = dict()
    if request.POST:

        if formset.is_valid():
            for form in formset:
                tag = form.cleaned_data.get('tag')
                if tag is not None:
                    try:
                        tag_obj = Tags.objects.get(tag=tag.strip())
                    except Exception:
                        tag_obj = Tags.objects.create(tag=tag.strip())
                    finally:
                        case = Case.objects.get(pk=pk)
                        case.tags.add(tag_obj)

            parameters, tag_list, pages = retrieve_cases(request)

            update_context = {
                'parameters': parameters,
                'tags': tag_list,
            }
            data['html_response'] = render_to_string('conteudo/includes/cards.html', update_context)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

    formset = TagsFormset()
    context = {
        'formset': formset,
        'pk': pk,
    }
    data['html_form'] = render_to_string(template, context, request=request)
    return JsonResponse(data)


class AddDoc(View):
    def get(self, request, pk):
        caso = Case.objects.get(pk=pk)
        titulo = caso.titulo
        return render(request, 'conteudo/add_docs.html', {'id': pk, 'titulo': titulo})

    def post(self, request, pk):
        file_list = list()
        try:
            case = Case.objects.get(pk=pk, user=request.user)
        except Exception as error:
            print(error)
        else:
            ids = request.POST['file-list-id'].split(';')
            for pk in ids:
                if pk is not '':
                    file_object = get_object_or_404(File, pk=pk)

                    criar_resumo(file_object.file, file_object)
                    # gerar_tags(file_object.resumo)

                    # passa as strings para a view
                    thumb = str(file_object.thumbnail.thumbnail.url)
                    file = str(file_object.file)
                    file_url = str(file_object.file)
                    file_list.append([file, [thumb, file_object.resumo]])

                    case.docs.add(file_object)

            return HttpResponseRedirect(reverse('conteudo:home'))


@method_decorator(login_required, name='dispatch')
class TemasView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {
            'tema_form': TemaForm(),
            'edit_form': EditTemaForm(),
        }
        return render(request, 'admin/temas/index.html', context)

    def post(self, request):
        tema_form = TemaForm(request.POST)


    def upload_file_tema(self, request, pk):

        data = dict()
        if request.POST:
            tema = Tema.objects.get(pk=pk)
            s3_file = PublicMediaStorage()
            s3_file.file_overwrite = False

            for file in request.FILES.getlist('files'):
                arquivo = unicodedata.normalize('NFD', str(file)).encode('ASCII', 'ignore').decode('ASCII')
                path = '%s/%s/%s' % (str(tema.identifier_code), str(pk), arquivo)
                uploaded_file = s3_file.save(path, file)
                save_file = File.objects.create(file=uploaded_file)

                tema.documentos.add(save_file)
                tema.save()

            return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class CaseAdminView(TemplateView):
    from .forms import CaseAdminForm

    def get(self, request, *args, **kwargs):
        context = {
            'case_form': self.CaseAdminForm(),
            # 'edit_form': EditTemaForm(),
        }
        return render(request, 'admin/cases/index.html', context)

    def post(self, request):
        if request.POST['mode'] == '1':
            resultado = self.upload_files(request)
            titulo = request.POST['titulo']
            resumo = request.POST['resumo']
            user = User.objects.get(pk=request.POST['user'])

            case = Case.objects.create(titulo=titulo, resumo=resumo, user=user)
            for file in resultado:
                case.docs.add(file)
            case.save()

            return HttpResponseRedirect(reverse('cases_admin:casos'))
        elif request.POST['mode'] == '2':
            self.create_case_by_title(request, request.POST['titulo'])

            return HttpResponseRedirect(reverse('cases_admin:casos'))

    def upload_files(self, request):
        file_list = list()
        if request.POST:
            s3_file = PublicMediaStorage()
            s3_file.file_overwrite = False

            s3_thumb = ThumbnailStorage()
            s3_thumb.file_overwrite = False
            i = 0
            for file in request.FILES.getlist('docs'):
                if not file.size > 5000000:
                    try:
                        pdf = wi(file=file, resolution=200)
                        arquivo = unicodedata.normalize('NFD', str(file)).encode('ASCII', 'ignore').decode('ASCII')
                        path = '%s/%s' % (str(request.user.pk), arquivo)
                        uploaded_file = s3_file.save(path, file)
                        save_file = File.objects.create(file=uploaded_file)
                    except Exception as error:
                        print(error)
                    else:
                        if save_file:
                            file_list.append(save_file)

                        try:
                            thumbnail_image = pdf.convert("jpeg")
                            temp_image = tempfile.SpooledTemporaryFile()
                            pdf_name = str(arquivo).split('.pdf')
                            thumb_name = '%s.jpg' % pdf_name[0]

                            with thumbnail_image.sequence[0] as img:
                                page = wi(image=img)
                                page.width = 150
                                page.height = 200
                                page.strip()
                                page.save(file=temp_image)
                                img_file = s3_thumb.save(thumb_name, temp_image)
                                thumbnail = Thumbnail.objects.create(thumbnail=img_file)
                                save_file.thumbnail = thumbnail
                                save_file.save()
                        except Exception as error:
                            print(error)
                i += 1

            return file_list

    def create_case_by_title(self, request, title):
        """
        Creates the case with the title to be the main folder, and subsequent files to be inside.
        Allows the upload of multiple files to extract text with AWS Lambda integration on S3.
        :param request: Request
        :param title: Title of the case/card
        :return: Nothing
        """
        if request.POST:
            user = User.objects.get(pk=request.POST['user'])
            case = Case.objects.create(titulo=title, user=user)
            s3_file = PublicMediaStorage()
            s3_file.file_overwrite = False

            for file in request.FILES.getlist('docs'):
                try:
                    arquivo = unicodedata.normalize('NFD', str(file)).encode('ASCII', 'ignore').decode('ASCII')
                    # Selected user ID
                    path = '%s/%s/%s/%s' % (str(user.pk), str(case.pk), title, arquivo)
                    uploaded_file = s3_file.save(path, file)
                    file_uploaded = File.objects.create(file=uploaded_file)
                    case.docs.add(file_uploaded)
                except Exception as error:
                    print(error)

            case.save()

        return True


def get_tema_admin(request):

    if request.POST:
        data = dict()
        try:
            tema = get_object_or_404(Tema, pk=request.POST['item'])
        except Exception as error:
            print(error)
        else:
            edit_form = TemaForm(instance=tema)
            context = {
                'form': edit_form,
            }
            data['html_response'] = render_to_string('includes/profile_form.html', context, request=request)
            data['is_valid'] = True
            return JsonResponse(data)


def edit_tema(request):
    if request.POST:
        tema = TemaForm(request.POST)
        if tema.is_valid():
            tema.save()
            return HttpResponseRedirect(reverse('temas_admin:temas'))


def filter_by_word(request, word):
    filtered_cases = Case.objects.filter(user=request.user, titulo__istartswith=word).order_by('titulo')
    parameters, tag_list = list(), list()
    for case in filtered_cases:
        if len(case.resumo) > 411:
            resumo = '%s ...' % case.resumo[0:411]
            fit = True
        else:
            resumo = case.resumo
            fit = False
        param_dict = {
            'titulo': case.titulo,
            'resumo': resumo,
            'fit': fit,
            'possible_edit': True,
        }
        parameters.append([case.pk, param_dict])
        for tag in case.tags.all():
            tag_list.append([case.pk, [tag.__str__()]])

    user_themes, all_themes = retrieve_themes(request)

    context = {
        'parameters': parameters,
        'tags': tag_list,
        'themes': user_themes,
    }
    return render(request, 'conteudo/home.html', context)


def filter_by_sentence(request, sentence):
    filtered_cases = Case.objects.filter(docs__resumo__icontains=sentence)
    parameters, tag_list = list(), list()
    for case in filtered_cases:
        if len(case.resumo) > 411:
            resumo = '%s ...' % case.resumo[0:411]
            fit = True
        else:
            resumo = case.resumo
            fit = False
        param_dict = {
            'titulo': case.titulo,
            'resumo': resumo,
            'fit': fit,
            'possible_edit': True,
        }
        parameters.append([case.pk, param_dict])
        for tag in case.tags.all():
            tag_list.append([case.pk, [tag.__str__()]])

    user_themes, all_themes = retrieve_themes(request)

    context = {
        'parameters': parameters,
        'tags': tag_list,
        'themes': user_themes,
    }
    return render(request, 'conteudo/home.html', context)


def filter_by_anything(request, sentence):

    filtered_cases = Case.objects.filter(titulo__icontains=sentence)
    if not filtered_cases:
        filtered_cases = Case.objects.filter(docs__resumo__icontains=sentence)

    parameters, tag_list = list(), list()
    for case in filtered_cases:
        if len(case.resumo) > 411:
            resumo = '%s ...' % case.resumo[0:411]
            fit = True
        else:
            resumo = case.resumo
            fit = False
        param_dict = {
            'titulo': case.titulo,
            'resumo': resumo,
            'fit': fit,
            'possible_edit': True,
        }
        parameters.append([case.pk, param_dict])
        for tag in case.tags.all():
            tag_list.append([case.pk, [tag.__str__()]])

    user_themes, all_themes = retrieve_themes(request)

    context = {
        'parameters': parameters,
        'tags': tag_list,
        'themes': user_themes,
    }
    return render(request, 'conteudo/home.html', context)


def handle_file_upload(request, arquivo):

    # for arquivo in request.FILES.getlist('files'):
    filename = unicodedata.normalize('NFD', str(arquivo)).encode('ASCII', 'ignore').decode('ASCII')
    path = 'tmp/%s/%s' % (str(request.user.pk), filename)
    dir_path = 'tmp/%s/' % str(request.user.pk)
    if not os.path.exists(dir_path):
        os.mkdir(path, mode=0o777)
    with open(path, 'wb+') as destination:
        for chunk in arquivo.chunks():
            destination.write(chunk)
