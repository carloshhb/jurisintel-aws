import pt_core_news_sm
from textacy import similarity

from .jurisintel_resumidor import resumidor

nlp = pt_core_news_sm.load()


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
    for resumo_referencia in lista_resumos_escritorio:
        yield (
            lista_resumos_escritorio.index(resumo_referencia),
            similarity.word_movers(referencia,
                                   nlp(resumo_referencia),
                                   metric='canberra')
        )
