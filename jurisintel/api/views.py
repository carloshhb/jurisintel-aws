import re

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from conteudo.models import Case, File
from conteudo.nlp.jurisintel_resumidor import resumidor_from_texto as res
# Create your views here.

# Global Variable Settings
FILENAME = re.compile('([+a-zA-Z0-9\s_\\.\-\(\):])+(.pdf)$')

@csrf_exempt
def receive_data(request):
    """
    Receives data from AWS Lambda. The function extracts the text from the file uploaded and return it to EC2 server
    save content in database.
    :return: Status
    """
    clean_text = ''
    texto_completo = request.POST['texto']
    for word in texto_completo:
        if word != '\n':
            clean_text += word

    text = clean_text.split()
    ftext = ''
    for word in text:
        if ftext == '':
            ftext += word
        else:
            ftext += ' ' + word

    if request.POST['case_id'] is not None:
        resumo = criar_resumo(ftext, request.POST['case_id'], request.POST['file_name'])
    else:
        resumo = criar_resumo(ftext, filename=request.POST['file_name'])

    return resumo


def criar_resumo(texto, pk=None, filename=None):

    case = Case.objects.get(pk=pk)
    docs = case.docs.all()
    resumo = ''
    for doc in docs:
        file_name = re.search(FILENAME, str(doc.file))
        if file_name.group() == filename:
            resumo = res(texto)
            doc.resumo = resumo
            doc.save()

    return resumo
