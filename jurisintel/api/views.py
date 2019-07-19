import re
import unicodedata

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from conteudo.models import Case, File, Thumbnail
from conteudo.nlp.jurisintel_resumidor import resumidor_from_texto as res
from jurisintel.storage_backends import PublicMediaStorage, ThumbnailStorage

# Create your views here.

# Global Variable Settings
FILENAME = re.compile('([+a-zA-Z0-9\s_\\.\-\(\):\[\]\~])+(.pdf|.docx)$', flags=re.I)


@csrf_exempt
def receive_data(request):
    """
    Receives data from AWS Lambda. The function extracts the text from the
    file uploaded and return it to EC2 server save content in database.
    :return: Status
    """
    
    try:
        clean_text = ''
        texto_completo = request.POST['texto']
        text = texto_completo.split()
        thumbnail = False
        thumb_name = ''
        if len(request.FILES.getlist('file')) > 0:
            thumbnail = request.FILES['file']
            thumb_name = request.POST['thumb_name']
        for word in text:
            if word != '\n':
                clean_text += ' ' + word

        text = clean_text.split()

        # ftext = ''
        # for word in text:
        #     if ftext == '':
        #         ftext += word
        #     else:
        #         ftext += ' ' + word

        if request.POST['case_id'] is not None:
            if thumbnail:
                resumo = criar_resumo(texto_completo, request.POST['case_id'], request.POST['file_name'], thumbnail=thumbnail, thumb_name=thumb_name)
            else:
                resumo = criar_resumo(texto_completo, request.POST['case_id'], request.POST['file_name'], thumbnail=None, thumb_name=thumb_name)
        # else:
        #     resumo = criar_resumo(clean_text, filename=request.POST['file_name'], thumbnail=thumbnail, thumb_name=thumb_name)

        data = {
            'ftext': clean_text,
            'resumo': resumo,
        }

        return JsonResponse(data)
    except Exception as error:
        data = {
            'error': str(error)
        }
        return JsonResponse(data)


def criar_resumo(texto, pk=None, filename=None, thumbnail=None, thumb_name=None):

    s3_thumb = ThumbnailStorage()
    s3_thumb.file_overwrite = False
    if thumbnail:
        thumb = s3_thumb.save(thumb_name, thumbnail)

    case = Case.objects.get(pk=pk)
    docs = case.docs.all()

    for doc in docs:
        file_name = FILENAME.search(str(doc.file))
        if not doc.resumo:
            if file_name.group() == filename:
                resumo = res(texto)
                if len(resumo) > 10:
                    doc.resumo = resumo
                else:
                    doc.resumo = texto

                if thumbnail:
                    thumb_saved = Thumbnail.objects.create(thumbnail=thumb)
                    doc.thumbnail = thumb_saved

                doc.save()

                return doc.resumo

    return 'Arquivo não encontrado'


@csrf_exempt
def teste(request):
    user = User.objects.get(pk=45)
    title = request.POST['titulo']
    descricao = title
    case = Case.objects.create(user=user, titulo=title, resumo=descricao)

    s3_file = PublicMediaStorage()
    s3_file.file_overwrite = False

    for file in request.FILES.getlist('files'):
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
