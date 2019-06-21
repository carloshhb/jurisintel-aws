import pt_core_news_sm

from .jurisintel_acoes import acao, acao_from_text
from .jurisintel_names import find_names, find_names_from_text
from .jurisintel_padroes import resumo, resumo_texto

nlp = pt_core_news_sm.load()


def resumidor(arquivo):
    return str(acao(arquivo).upper() + " " + find_names(arquivo) + " " + resumo(arquivo))


def resumidor_from_texto(texto):
    return str(acao_from_text(texto).upper() + " " + find_names_from_text(texto) + " " + resumo_texto(texto))
