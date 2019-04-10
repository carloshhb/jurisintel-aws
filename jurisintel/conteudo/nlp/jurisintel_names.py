import itertools

import pt_core_news_sm
import slate3k as slate

nlp = pt_core_news_sm.load()


def names_seq(seq):
    return ('PROPN', 'PROPN', 'PROPN') in zip(seq, itertools.islice(seq, 1, None), itertools.islice(seq, 2, None))


def extract_text(file):
    f = open(file, 'rb')
    pdf = slate.PDF(f)

    brief = ''
    for item in pdf:
        brief += item

    return brief


def find_names(arquivo):
    peticao = extract_text(arquivo)
    dez_pc = int(len(peticao)/10)
    cabeca = peticao[:dez_pc]
    texto_nlp = nlp(cabeca)
    names = str()
    for token in texto_nlp:
        if token.pos_ == 'PUNCT':
            if names_seq((texto_nlp[token.i - 4].pos_, texto_nlp[token.i - 3].pos_, texto_nlp[token.i - 2].pos_, texto_nlp[token.i - 1].pos_)):
                names += texto_nlp[token.i - 4].text + " " + texto_nlp[token.i - 3].text + " " + texto_nlp[token.i - 2].text + " " + texto_nlp[token.i - 1].text + "\t"
    return names
