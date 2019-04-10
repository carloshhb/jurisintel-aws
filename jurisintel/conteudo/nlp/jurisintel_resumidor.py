import pt_core_news_sm

from .jurisintel_acoes import acao
from .jurisintel_names import find_names
from .jurisintel_padroes import resumo

nlp = pt_core_news_sm.load()


def resumidor(arquivo):
    return str(acao(arquivo).upper() + " " + find_names(arquivo) + " " + resumo(arquivo))


