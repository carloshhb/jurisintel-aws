import os
import unicodedata
import requests
import mimetypes
import tempfile
import secrets
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.template.loader import render_to_string
from wand.image import Image as wi

from jurisintel.storage_backends import PublicMediaStorage, ThumbnailStorage
from .forms import CardForm
from .models import Case, Files, Tags, Thumbnail
from .nlp.jurisintel_resumidor import resumidor as res
from .nlp.similar import similar_resumo
# Create your views here.


def upload(request):

    data = dict()

    if request.POST:
        s3_file = PublicMediaStorage()
        s3_file.file_overwrite = False

        s3_thumb = ThumbnailStorage()
        s3_thumb.file_overwrite = False

        for file in request.FILES.getlist('files'):
            pdf = wi(file=file, resolution=200)
            arquivo = unicodedata.normalize('NFD', str(file)).encode('ASCII', 'ignore').decode('ASCII')
            path = '%s/%s' % (str(request.user.pk), arquivo)
            uploaded_file = s3_file.save(path, file)
            save_file = Files.objects.create(file=uploaded_file)

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

            data = {
                'is_valid': True,
                'file_id': save_file.pk
            }

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

        return HttpResponseRedirect(reverse('home'))


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

        return HttpResponseRedirect(reverse('home'))


def remove(request):
    if request.POST:
        case = Case.objects.get(pk=request.POST['pk'])
        case.delete()

        return HttpResponseRedirect(reverse('home'))


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

        context = {
            'titulo': case.titulo,
            'resumo': case.resumo,
            'docs': docs,
            'tags': tags,
            'ementas': ementas,
            'pk': pk,
        }

        return render(request, 'conteudo/open_case.html', context)
    else:
        return HttpResponseRedirect(reverse('home'))


# def get_file(arquivo):
#     k = requests.get(arquivo.url, stream=True)
#     file_mimetype = mimetypes.guess_type(k.url)
#     if file_mimetype[0] == 'application/pdf':
#         # Nome do arquivo temporário
#         temp_filename = '%s.pdf' % random_name(10)
#         tmp_file = 'tmp/' + temp_filename
#         with open(tmp_file, "wb") as fd:
#             for chunk in k.iter_content(chunk_size=128):
#                 fd.write(chunk)
#         return tmp_file


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
