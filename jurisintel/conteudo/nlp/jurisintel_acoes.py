import pt_core_news_sm
import slate3k as slate
from spacy.matcher import PhraseMatcher

nlp = pt_core_news_sm.load()

matcher_acoes = PhraseMatcher(nlp.vocab)

dicionario_acoes = [
    'ação direta de inconstitucionalidade',
    'ação de usucapião',
    'ação de cobrança',
    'ação ordinária de cobrança',
    'ação civil pública',
    'ação de alimentos',
    'ação de adoção',
    'ação de emancipação',
    'ação de guarda',
    'embargos de terceiro',
    'habilitação para adoção',
    'mandado de segurança',
    'pedido de autorização judicial',
    'ação ordinária',
    'ação anulatória',
    'ação declaratória',
    'recurso de apelação',
    'apelação cível',
    'embargos à execução',
    'ação de despejo',
    'contestação',
]

dicio_acoes_nlp = []

for item in dicionario_acoes:
    txt_nlp = nlp(item.lower())
    dicio_acoes_nlp.append(txt_nlp)


matcher_acoes.add('Dicionário_Acoes', None, *dicio_acoes_nlp)


def extract_text(file):
    f = open(file, 'rb')
    pdf = slate.PDF(f)

    brief = ''
    for item in pdf:
        brief += item

    return brief


def acao(arquivo):
    peticao = extract_text(arquivo)
    num_corte = int(len(peticao)/10)
    corpo = peticao[:num_corte]
    txt_nlp = nlp(corpo.lower())
    matches = matcher_acoes(txt_nlp)
    if len(matches) == 0:
        return ' '
    if len(matches) > 0:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            return txt_nlp[start:end].string


def acao_from_text(texto):
    """
    Retira o nome da ação a partir de um texto gerado de um documento
    :param texto: Texto padrão UTF-8
    :return: Nome da ação (str)
    """
    num_corte = int(len(texto)/10)
    corpo = texto[:num_corte]
    txt_nlp = nlp(corpo.lower())
    matches = matcher_acoes(txt_nlp)
    if len(matches) == 0:
        return ' '
    if len(matches) > 0:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            return txt_nlp[start:end].string
