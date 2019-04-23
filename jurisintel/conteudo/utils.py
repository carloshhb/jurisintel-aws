# IMPORTS HERE IF NEEDED


# HELPER FUNCTIONS
def get_documents_(case):
    documentos = list()
    for doc in case.docs.all():
        docs_dict = {
            'file_name': str(doc.file).split('/')[1],
            'file_thumbnail': doc.thumbnail.thumbnail.url,
            'file_url': doc.file.url,
            'file_id': doc.pk,
        }
        documentos.append([doc.pk, docs_dict])

    return documentos


def get_case_tags(case):
    tags = list()
    for tag in case.tags.all():
        tags.append(tag)

    return tags


def get_case_ementas(case):

    ementas = list()
    for ementa in case.ementas.all():
        ementas.append(ementa)

    return ementas