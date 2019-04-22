import mimetypes
import os
import secrets
import tempfile
import unicodedata

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from jurisintel.storage_backends import PublicMediaStorage, ThumbnailStorage
from wand.image import Image as wi

from .forms import CardForm, UpdateCaseForm
from .models import Case, Files, Tags, Thumbnail
from .nlp.jurisintel_resumidor import resumidor as res
from .nlp.similar import similar_resumo


# Create your views here.


def retrieve_cases(request):
    parameters, tag_list = list(), list()

    all_cases = Case.objects.filter(user=request.user).order_by('-created_at')
    for case in all_cases:
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
        }
        parameters.append([case.pk, param_dict])
        for tag in case.tags.all():
            tag_list.append([case.pk, [tag.__str__()]])

    return parameters, tag_list


@login_required(login_url='user_login')
def home(request):

    parameters, tag_list = retrieve_cases(request)

    context = {
        'parameters': parameters,
        'tags': tag_list,
    }

    return render(request, 'conteudo/home.html', context)


def upload(request):

    data = dict()

    if request.POST:
        s3_file = PublicMediaStorage()
        s3_file.file_overwrite = False

        s3_thumb = ThumbnailStorage()
        s3_thumb.file_overwrite = False

        for file in request.FILES.getlist('files'):
            try:
                pdf = wi(file=file, resolution=200)
                arquivo = unicodedata.normalize('NFD', str(file)).encode('ASCII', 'ignore').decode('ASCII')
                path = '%s/%s' % (str(request.user.pk), arquivo)
                uploaded_file = s3_file.save(path, file)
                save_file = Files.objects.create(file=uploaded_file)
            except Exception as error:
                print(error)
            else:
                if save_file:
                    data['is_valid'] = True
                    data['file_id'] = save_file.pk
                else:
                    data['is_valid'] = False

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

        return JsonResponse(data)


def random_name(size):
    return secrets.token_hex(size)


def criar_resumo(arquivo, objeto):
    k = requests.get(arquivo.url, stream=True)
    file_mimetype = mimetypes.guess_type(k.url)
    if file_mimetype[0] == 'application/pdf':
        # Nome do arquivo temporário
        temp_filename = '%s.pdf' % random_name(10)
        tmp_file = 'tmp/' + temp_filename
        with open(tmp_file, "wb") as fd:
            for chunk in k.iter_content(chunk_size=128):
                fd.write(chunk)

        objeto.resumo = res(tmp_file)
        objeto.save()

        # Remover o arquivo temporário
        os.remove(tmp_file)


def file_upload(request):

    file_list = list()
    form = CardForm()

    if request.POST:
        # Criar o caso antes, e se não confirmar na proxima tela, remover
        pre_case = Case.objects.create(user=request.user)

        ids = request.POST['file-list-id'].split(';')
        for pk in ids:
            if pk is not '':
                file_object = get_object_or_404(Files, pk=pk)

                criar_resumo(file_object.file, file_object)
                # gerar_tags(file_object.resumo)

                # passa as strings para a view
                thumb = str(file_object.thumbnail.thumbnail.url)
                file = str(file_object.file)
                file_url = str(file_object.file)
                file_list.append([file, [thumb, file_object.resumo]])

                pre_case.docs.add(file_object)

        context = {
            'files': file_list,
            'form': form,
            'pre_case_id': pre_case.pk
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
    if request.user == case.user:

        docs = list()
        for doc in case.docs.all():
            docs.append(doc)

        tags = list()
        for tag in case.tags.all():
            tags.append(tag)

        ementas = list()
        for ementa in case.ementas.all():
            ementas.append(ementa)

        tamanho_resumo = len(case.resumo)
        if tamanho_resumo > 730:
            resumo_fit = '%s ...' % case.resumo[0:730]
        else:
            resumo_fit = ''

        context = {
            'titulo': case.titulo,
            'resumo_fit': resumo_fit,
            'resumo': case.resumo,
            'docs': docs,
            'tags': tags,
            'ementas': ementas,
            'pk': pk,
        }

        return render(request, 'conteudo/open_case.html', context)
    else:
        return HttpResponseRedirect(reverse('conteudo:home'))


def verify_similarities(request, pk):
    if request.POST:
        file_to_verify = Files.objects.get(pk=request.POST['file'])
        list_of_files = Files.objects.filter(case__user=request.user).exclude(file=file_to_verify)

        resumo_referencia = file_to_verify.resumo

        filtered_list, filtered_list_ids = list(), list()

        for file in list_of_files:
            filtered_list.append(file.resumo)
            filtered_list_ids.append(file.pk)

        similares = similar_resumo(resumo_referencia, filtered_list)

        indices = list()

        for s in similares:
            indices.append([s[1], filtered_list[s[0]], filtered_list_ids[s[0]]])

        indices.sort(key=lambda x: x[0], reverse=True)

        simm = list()
        for k in indices:
            f = Files.objects.get(pk=k[2])
            simdict = {
                'file_name': str(f.file).split('/')[1],
                'indice_sim': k[0],
                'file_url': str(f.file.url),
                'thumbnail': str(f.thumbnail.thumbnail.url),
            }
            simm.append([f.pk, simdict])

        context = {'resultado': simm}
        data = {
            'html_resultado': render_to_string('conteudo/includes/similares_resultado.html', context=context, request=request)
        }

        return JsonResponse(data)

    else:
        case = get_object_or_404(Case, pk=pk)

        docs = list()
        for doc in case.docs.all():
            docs.append([str(doc.file), [str(doc.thumbnail.thumbnail.url), doc.pk]])

        data = dict()
        context = {
            'docs': docs,
            'pk': pk,
        }
        data['html_similares'] = render_to_string(template_name='conteudo/includes/similares.html', context=context,
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

            parameters, tag_list = retrieve_cases(request)

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


def save_(request, form, template):

    data = dict()

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            data['form_is_valid'] = True

            parameters, tag_list = retrieve_cases(request)

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
                    file_object = get_object_or_404(Files, pk=pk)

                    criar_resumo(file_object.file, file_object)
                    # gerar_tags(file_object.resumo)

                    # passa as strings para a view
                    thumb = str(file_object.thumbnail.thumbnail.url)
                    file = str(file_object.file)
                    file_url = str(file_object.file)
                    file_list.append([file, [thumb, file_object.resumo]])

                    case.docs.add(file_object)

            return HttpResponseRedirect(reverse('conteudo:home'))
