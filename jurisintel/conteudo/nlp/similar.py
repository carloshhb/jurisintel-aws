import pt_core_news_sm
from textacy import similarity

from .jurisintel_resumidor import resumidor
from ..models import Tags

nlp = pt_core_news_sm.load()

# Tags theme list

list_of_tags = [
    'Direito Tributário',
    'Princípios Constitucionais',
    'Suspensão da Exigibilidade do Crédito Tributário',
    'Espécies Tributárias',
    'Extinção da Exigibilidade do Crédito Tributário',
    'Competência',
    'Capacidade Tributária',
    'Imunidades',
    'Isenção',
    'Fraude à Execução',
    'IPVA',
    'ICMS',
    'Garantias',
    'Privilégios do Crédito Tributário',
    'IPTU',
    'ITR',
    'Obrigação Tributária',
    'Classificação dos Tributos',
    'SIMPLES',
    'Repartição Constitucional de Receitas',
    'IPI',
    'IR',
    'Extinção do crédito tributário',
    'Compensação',
    'Remissão',
    'Transação',
    'Decadência',
    'Prescrição',
    'Exclusão do crédito tributário',
    'Garantias do crédito tributário',
    'Privilégios do crédito tributário',
    'Processo administrativo tributário',
    'Impostos',
    'Execução fiscal'
]

tags_obj = Tags.objects.all()
for k in list_of_tags:
    try:
        Tags.objects.get(tag=k)
    except Exception as exception:
        Tags.objects.create(tag=k)


def similar(arquivo_referencia, lista_pets_escritorio):
    referencia = nlp(resumidor(arquivo_referencia))
    for peticao_referencia in lista_pets_escritorio:
        yield (
            lista_pets_escritorio.index(peticao_referencia),
            similarity.word_movers(referencia,
                                   nlp(resumidor(peticao_referencia)),
                                   metric='canberra'))


def similar_resumo(resumo_referencia, lista_resumos_escritorio):
    referencia = nlp(resumo_referencia)
    for ref in lista_resumos_escritorio:
        yield (
            lista_resumos_escritorio.index(ref),
            similarity.word_movers(referencia,
                                   nlp(ref),
                                   metric='canberra')
        )


def similar_tags(resumo_ref, tag_list):
    referencia = nlp(resumo_ref)
    for ref in tag_list:
        yield (
            tag_list.index(ref),
            similarity.word_movers(referencia,
                                   nlp(ref),
                                   metric='canberra')
        )
