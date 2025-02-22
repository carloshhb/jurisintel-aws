# IMPORTS HERE IF NEEDED
import re
import pytesseract
import subprocess
import slate3k as slate
from PIL import Image

# HELPER FUNCTIONS

TAG_RE = re.compile(r'<[^>]+>')
FILENAME = re.compile('([+a-zA-Z0-9\s_\\.\-\(\):\[\]\~])+(.pdf|.docx)$', flags=re.I)


def get_documents_(case):
    documentos = list()
    for doc in case.docs.all():
        try:
            filename = FILENAME.search(str(doc.file)).group()
            docs_dict = {
                'file_name': filename,
                'file_thumbnail': doc.thumbnail.thumbnail.url,
                'file_resumo': doc.resumo,
                'file_url': doc.file.url,
                'file_id': doc.pk,
            }
        except Exception:
            filename = FILENAME.search(str(doc.file)).group()
            docs_dict = {
                'file_name': filename,
                'file_thumbnail': 'docx',
                'file_resumo': doc.resumo,
                'file_url': doc.file.url,
                'file_id': doc.pk,
            }
        documentos.append([doc.pk, docs_dict])

    return documentos


def get_documents_tema(tema):
    documentos = list()
    for doc in tema.documentos.all():
        docs_dict = {
            'file_name': str(doc.file),
            'file_thumbnail': doc.thumbnail.thumbnail.url,
            'file_url': doc.file.url,
            'file_id': doc.pk,
        }
        documentos.append([doc.pk, docs_dict])

    return documentos


def get_info_file(file, indice):
    """
    Get informations of each file
    :param file: File object
    :param indice: Index of file in list
    :return: Dict
    """
    filename = FILENAME.search(str(file.file)).group()
    if file.thumbnail is not None:
        simdict = {
            'file_name': filename,
            'indice_sim': indice,
            'file_url': str(file.file.url),
            'thumbnail': str(file.thumbnail.thumbnail.url),
        }
    else:
        simdict = {
            'file_name': filename,
            'indice_sim': indice,
            'file_url': str(file.file.url),
            'thumbnail': 'docx',
        }
    return simdict


def get_case_tags(case):
    tags = list()
    for tag in case.tags.all():
        tags.append(tag)

    return tags


def get_case_ementas(case):

    ementas = list()
    for ementa in case.ementas.all():
        ementa_dict = {
            'ementa_orgao': ementa.orgao,
            'ementa_texto': TAG_RE.sub('', ementa.texto),
        }
        ementas.append(ementa_dict)

    return ementas


def get_printable_size(byte_size):
    """
    A bit is the smallest unit, it's either 0 or 1
    1 byte = 1 octet = 8 bits
    1 kB = 1 kilobyte = 1000 bytes = 10^3 bytes
    1 KiB = 1 kibibyte = 1024 bytes = 2^10 bytes
    1 KB = 1 kibibyte OR kilobyte ~= 1024 bytes ~= 2^10 bytes (it usually means 1024 bytes but sometimes it's 1000... ask the sysadmin ;) )
    1 kb = 1 kilobits = 1000 bits (this notation should not be used, as it is very confusing)
    1 ko = 1 kilooctet = 1000 octets = 1000 bytes = 1 kB
    Also Kb seems to be a mix of KB and kb, again it depends on context.
    In linux, a byte (B) is composed by a sequence of bits (b). One byte has 256 possible values.
    More info : http://www.linfo.org/byte.html
    """
    BASE_SIZE = 1024.00
    MEASURE = ["B", "KB", "MB", "GB", "TB", "PB"]

    def _fix_size(size, size_index):
        if not size:
            return "0"
        elif size_index == 0:
            return str(size)
        else:
            return "{:.3f}".format(size)

    current_size = byte_size
    size_index = 0

    while current_size >= BASE_SIZE and len(MEASURE) != size_index:
        current_size = current_size / BASE_SIZE
        size_index = size_index + 1

    size = _fix_size(current_size, size_index)
    measure = MEASURE[size_index]
    return size + measure


def tesseract_extract(arquivo):
    resultado = pytesseract.image_to_string(Image.open(arquivo), lang='por')
    return resultado


def antiword_extract(arquivo):
    try:
        command = 'antiword {}'.format(
            arquivo,
            'stdout',
        )
        try:
            print('Start')
            output = subprocess.check_output(command, env={'ANTIWORDHOME': '/usr/share/antiword'}, shell=True, stderr=subprocess.STDOUT)
            print('Finish')

        except subprocess.CalledProcessError as e:
            print('Error')
            print(e.output)
            return e.output

    except Exception as e:
        print('Error e')
        print(e)
        raise e
    return output


def parse_pdfminer(file):
    with open(file, 'rb') as f:
        doc = slate.PDF(f)

    texto = ''
    for item in doc:
        texto += item

    if len(texto) > 50:
        return texto
    else:
        raise ValueError
