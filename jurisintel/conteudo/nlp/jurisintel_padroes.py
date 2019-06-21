import pt_core_news_sm
import slate3k as slate
from spacy.matcher import Matcher
from textacy import keyterms

nlp = pt_core_news_sm.load()


def extract_text(file):

    with open(file, 'rb') as f:
        pdf = slate.PDF(file=f)

    brief = ''
    for item in pdf:
        brief += item

    return brief


def resumo(arquivo):
    peticao = extract_text(arquivo)
    dez_pc = int(len(peticao)/10)
    corpo = peticao[dez_pc:(-1 * (dez_pc))]
    termos = set()
    texto_nlp = nlp(corpo)
    for expressao, indice in keyterms.key_terms_from_semantic_network(texto_nlp, normalize='lower', window_width=5,
                                                                      edge_weighting='cooc_freq', join_key_words=True,
                                                                      n_keyterms=0.002):
            termos.add(expressao)
    matches = matcher(texto_nlp)
    for match_id, start, end in matches:
        span = texto_nlp[start:end]
        termos.add(span.text.lower())
    res = str()
    for expressao in keyterms.aggregate_term_variants(termos, fuzzy_dedupe=True):
        res += str((sorted(list(expressao), key=len)[-1])).capitalize() + '. '

    return res


def resumo_texto(texto):
    dez_pc = int(len(texto) / 10)
    corpo = texto[dez_pc:(-1 * (dez_pc))]
    termos = set()
    texto_nlp = nlp(corpo)
    for expressao, indice in keyterms.key_terms_from_semantic_network(texto_nlp, normalize='lower', window_width=5,
                                                                      edge_weighting='cooc_freq', join_key_words=True,
                                                                      n_keyterms=0.002):
        termos.add(expressao)
    matches = matcher(texto_nlp)
    for match_id, start, end in matches:
        span = texto_nlp[start:end]
        termos.add(span.text.lower())
    res = str()
    for expressao in keyterms.aggregate_term_variants(termos, fuzzy_dedupe=True):
        res += str((sorted(list(expressao), key=len)[-1])).capitalize() + '. '

    return res

matcher = Matcher(nlp.vocab)

# LISTA GERAL DOS PADRÕES - ARTS


lista_arts_lei_geral = [
    
# Rule 01
# art. 9º da Lei 13.234/18
# art 9º da Lei 13.234/18
# art 15 da Lei 13.234/18
# art. 15 da Lei 13.234/18
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],

#Rule 02
# art. 9º da Lei n. 13.234/18s
# art. 15 da Lei n. 13.234/18
# art. 15 da Lei n.º 13.234/18
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],   

#Rule 03
# arts. 15 e 16 da Lei 13.234/18
# arts 15 e 16 da Lei 13.234/18
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],

#Rule 04
# arts 15 e 16 da Lei n. 13.234/18 
# arts 15 e 16 da Lei nº 13.234/18
# arts 15 e 16 da Lei n.º 13.234/18
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],
  
#Rule 05
# arts 15, 17 e 16 da Lei 13.234/18
# arts 15, 17, 16 da Lei 13.234/18
# arts. 15, 17, 16 da Lei 13.234/18
# arts. 15, 17 e 16 da Lei 13.234/18
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],

#Rule 06    
# arts. 15, 17 e 16 da Lei n. 13.234/18
# arts. 15, 17 e 16 da Lei nº 13.234/18
# arts. 15, 17, 16 da Lei nº 13.234/18
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 07
# art. 15, Lei 1.234/00
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN', 'OP':'?'}, {'POS': 'PROPN', 'OP': '?'}],

#Rule 08
# art. 15, Lei n. 1.234/00
# art. 15, Lei nº 1.234/00
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 09
# inciso V do art. 15 da Lei 1.234/00
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN', 'OP':'?'}, {'POS': 'PROPN', 'OP': '?'}],

#Rule 10
# inciso V do art. 15 da Lei n. 1.234/00 
# inciso V do art. 15 da Lei nº 1.234/00
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 11
# incisos II e V do art. 15 da Lei 1.234/00
[{'LOWER': 'incisos'}, {}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN', 'OP':'?'}, {'POS': 'PROPN', 'OP': '?'}],    

#Rule 12
# incisos II, V e VII do art. 15 da Lei 1.234/00
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN', 'OP':'?'}, {'POS': 'PROPN', 'OP': '?'}],

#Rule 13
# incisos II e VII do art. 15 da Lei n. 1.234/00
# incisos II e VII do art. 15 da Lei nº 1.234/00
[{'LOWER': 'incisos'}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 14   
# inciso I, do art. 165, da Lei 1.234/00
[{'LOWER': 'inciso'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'VERB'}],
    
#Rule 15
# inciso I, do art. 15, da Lei nº 1.234/00
[{'LOWER': 'inciso'}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM', 'OP': '?'}],

#Rule 16
# art. 44, inciso II, da Lei nº 9.430
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],

#Rule 17
# art. 44, inciso I, da Lei 9.430
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}],

#Rule 18
# art. 44, incisos I e II, da Lei 9.430
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}],

#Rule 19
# art. 44, incisos I, II e III, da Lei 9.430
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP':'?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}, {'POS': 'NUM', 'OP': '?'}],
 
#Rule 20
# art. 44, incisos II e III, da Lei nº 9.430
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],

#Rule 21
# art. 44, incisos II, III e IV, da Lei nº 9.430    
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],

#Rule 22
# inc. V do art. 15 da Lei 1.234/00
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'lei'}, {'POS': 'NUM'}],

#Rule 23
# inc. V do art. 15 da Lei n. 1.234/00
# inc. V do art. 15 da Lei nº 1.234/00
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],
    
#Rule 24
# incs. V e VII do art. 15 da Lei 1.234/00    
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'lei'}, {'POS': 'NUM'}],
  
#Rule 25
# incs. V, VI e VII do art. 15 da Lei 1.234/00
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},{}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'lei'}, {'POS': 'NUM'}],

#Rule 26
# incs. V e VII do art. 15 da Lei n. 1.234/00 
# incs. V e VII do art. 15 da Lei nº 1.234/00
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],
 
#Rule 27
# incs. V, VI e VII do art. 15 da Lei nº 1.234/00   
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},{}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],

#Rule 28
# arts. 2° e 13 da mencionada Lei 8.035/90
# arts. 21 e 13 da mencionada Lei 8.035/90
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'PROPN', 'OP': '?'}, {}, {}, {'POS': 'ADP'}, {}, {'LOWER': 'lei'}, {}],
    
#Rule 29
# § 1º do art. 21 da Lei 8.035/90
[{'ORTH': '§'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {}],

#Rule 30
# §§ 1º e 2º do art. 21 da Lei 8.035/90
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {}],
    
#Rule 31
# § 1º do art. 21 da Lei n. 8.035/90
# § 1º do art. 21 da Lei nº 8.035/90
[{'ORTH': '§'}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {}, {}],
  
#Rule 32
# §§ 1º e 2º do art. 21 da Lei nº 8.035/90
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {}, {}],

#Rule 33
# art. 21, § 2º, da Lei 8.035/90
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {}],    
   
#Rule 34
# art. 21, § 2º, da Lei nº 8.035/90
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {}, {}],
   
#Rule 35
# art. 21, §§ 2º e 3º, da Lei 8.035/90    
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {}], 
 
#Rule 36
# art. 21, §§ 2º e 3º, da Lei nº 8.035/90
# art. 21, §§ 2º e 3º, da Lei n. 8.035/90
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {}, {}],
 
#Rule 37
# art. 44, parágrafo 1º, da Lei nº 9.430
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],

#Rule 38
# art. 44, parágrafo 1º, da Lei 9.430
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}],

#Rule 39
# art. 44, parágrafos 2º e 3º, da Lei 9.430
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}],

#Rule 40
# art. 44, parágrafos 2º e 3º, da Lei nº 9.430
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],
    
#Rule 41
# art. 44, parágrafos 2º e 3º, da Lei n. 9.430    
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'PROPN', 'OP': '?'}],

#Rule 42
# parágrafo 2º do art. 5º da Lei 9.430    
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'lei'}, {}],
 
#Rule 43
# parágrafo 2º do art. 5º da Lei nº 9.430/90
# parágrafo 2º do art. 5º da Lei n. 9.430/90 
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],
  
#Rule 44
# art. 5º, parágrafo 1º, alínea "a" da Lei nº 9.430/90
# art. 5º, parágrafo 1º, alínea a da Lei n. 9.430/90
# art. 5º, parágrafo 1º, alínea A da Lei 1.234/90
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'lei'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NOUN', 'OP': '?'}, {}],   

#Rule 45
# art. 5º, § 1º, "a", da Lei nº 1.234/90
# art. 5º, § 1º, "a", da Lei n. 1.234/90
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'LOWER': 'lei'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NOUN', 'OP': '?'}, {}],
 
#Rule 46
# art. 5º, § 1º, "a", da Lei 1.234/90
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {'POS': 'NUM'}],
    
#Rule 47
# art. 5º, § 1º, alínea "a", da Lei 1.234/90
# art. 5º, § 1º, alínea a, da Lei 1.234/90
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {'POS': 'NUM'}],

#Rule 48
# art. 5º, § 1º, alínea a, da Lei nº 1.234/90
# art. 5º, § 1º, alínea "a", da Lei nº 1.234/90
# art. 5º, § 1º, alínea a, da Lei n. 1.234/90
# art. 5º, § 1º, alínea "a", da Lei n. 1.234/90
# art. 5º, § 1º, alínea "a", da Lei 1.234/90
# art. 5º, § 1º, alínea a, da Lei 1.234/90
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 49
# § 1º, "a", do art. 15 da Lei 1.234/90
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}],
 
#Rule 50
# § 1º, a, do art. 15 da Lei n. 1.234/90
# § 1º, a, do art. 15 da Lei nº 1.234/90
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM'}],

#Rule 51
# "a", § 1º, do art. 15 da Lei 1.234/90
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'lei'}, {}],
    
#Rule 52
# "a", § 1º, do art. 15 da Lei n. 1.234/90
# "a", § 1º, do art. 15 da Lei nº 1.234/90
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM'}]    
    
]

# LISTA GERAL DOS PADRÕES - ARTIGOS


lista_artigos_lei_geral = [
    
# Rule 53
# artigo 9º da Lei 13.234/18
# artigo 9º da Lei 13.234/18
# artigo 15 da Lei 13.234/18
# artigo 15 da Lei 13.234/18
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],

#Rule 54
# artigo 9º da Lei n. 13.234/18
# artigo 15 da Lei n. 13.234/18
# artigo 15 da Lei n.º 13.234/18
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],   

#Rule 55
# artigos 15 e 16 da Lei 13.234/18
# artigos 15 e 16 da Lei 13.234/18
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],

#Rule 56
# artigos 15 e 16 da Lei n. 13.234/18 
# artigos 15 e 16 da Lei nº 13.234/18
# artigos 15 e 16 da Lei n.º 13.234/18
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],
  
#Rule 57
# artigos 15, 17 e 16 da Lei 13.234/18
# artigos 15, 17, 16 da Lei 13.234/18
# artigos 15, 17, 16 da Lei 13.234/18
# artigos 15, 17 e 16 da Lei 13.234/18
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],

#Rule 58
# artigos 15, 17 e 16 da Lei n. 13.234/18
# artigos 15, 17 e 16 da Lei nº 13.234/18
# artigos 15, 17, 16 da Lei nº 13.234/18
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 59
# artigo 15, Lei 1.234/00
[{'LOWER': 'art'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN', 'OP':'?'}, {'POS': 'PROPN', 'OP': '?'}],

#Rule 60
# artigo 15, Lei n. 1.234/00
# artigo 15, Lei nº 1.234/00
[{'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 61
# inciso V do artigo 15 da Lei 1.234/00
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN', 'OP':'?'}, {'POS': 'PROPN', 'OP': '?'}],

#Rule 62
# inciso V do artigo 15 da Lei n. 1.234/00 
# inciso V do artigo 15 da Lei nº 1.234/00
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 63
# incisos II e V do artigo 15 da Lei 1.234/00
[{'LOWER': 'incisos'}, {}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN', 'OP':'?'}, {'POS': 'PROPN', 'OP': '?'}],    

#Rule 64
# incisos II, V e VII do artigo 15 da Lei 1.234/00
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {'POS': 'NUM', 'OP':'?'}, {'POS': 'PROPN', 'OP':'?'}, {'POS': 'PROPN', 'OP': '?'}],

#Rule 65
# incisos II e VII do artigo 15 da Lei n. 1.234/00
# incisos II e VII do artigo 15 da Lei nº 1.234/00
[{'LOWER': 'incisos'}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 66 
# inciso I, do artigo 165, da Lei 1.234/00
[{'LOWER': 'inciso'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'VERB'}],
    
#Rule 67
# inciso I, do artigo 15, da Lei nº 1.234/00
[{'LOWER': 'inciso'}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'lei'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NUM', 'OP': '?'}],

#Rule 68
# artigo 44, inciso II, da Lei nº 9.430
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],

#Rule 69
# artigo 44, inciso I, da Lei 9.430
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}],

#Rule 70
# artigo 44, incisos I e II, da Lei 9.430
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}],

#Rule 71
# artigo 44, incisos I, II e III, da Lei 9.430
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP':'?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}, {'POS': 'NUM', 'OP': '?'}],
 
#Rule 72
# artigo 44, incisos II e III, da Lei nº 9.430
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],

#Rule 73
# artigo 44, incisos II, III e IV, da Lei nº 9.430    
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],

#Rule 74
# inc. V do artigo 15 da Lei 1.234/00
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'lei'}, {}],

#Rule 75
#inc. V do artigo 15 da Lei n. 1.234/00
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {}],
    
# Rule 76
# incs. V e VII do artigo 15 da Lei 1.234/00
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {}],

# Rule 77
# incs. V, VI e VII do artigo 15 da Lei 1.234/00
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {}],
    
# Rule 78
# incs. V e VII do artigo 15 da Lei n. 1.234/00 
# incs. V e VII do artigo 15 da Lei nº 1.234/00
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {}, {}],
    
# Rule 79
# artigos 2° e 13 da mencionada Lei 8.035/90
# artigos 21 e 13 da mencionada Lei 8.035/90
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'PROPN', 'OP': '?'}, {}, {}, {'POS': 'ADP'}, {}, {'LOWER': 'lei'}, {}],

# Rule 80
# artigos 2º e 12 da Lei 8.035/1990
# artigos 2º e 9º da Lei 8.035/1990
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {}],
    
# Rule 81
# artigos 2º, 5º e 12 da Lei 8.035/1990 Lembrar que em vários lugares há regras que terminam por capturar em duplicidade
# artigos 2º, 5º e 12 da Lei 8.035/90
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'lei'}, {}],
    
#Rule 82
# § 1º do artigo 21 da Lei 8.035/90
[{'ORTH': '§'}, {}, {}, {'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {}],

#Rule 83
# §§ 1º e 2º do artigo 21 da Lei 8.035/90
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {}],
    
#Rule 84
# § 1º do artigo 21 da Lei n. 8.035/90
[{'ORTH': '§'}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {}, {}],
  
#Rule 85
# §§ 1º e 2º do artigo 21 da Lei nº 8.035/90
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {}, {}],

#Rule 86
# artigo 21, § 2º, da Lei 8.035/90
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {}],    
   
#Rule 87
# artigo 21, § 2º, da Lei nº 8.035/90
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {}, {}],
   
#Rule 88
# artigo 21, §§ 2º e 3º, da Lei 8.035/90    
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {}], 
 
#Rule 89
# artigo 21, §§ 2º e 3º, da Lei nº 8.035/90
# artigo 21, §§ 2º e 3º, da Lei n. 8.035/90
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {}, {}],
 
#Rule 90
# artigo 44, parágrafo 1º, da Lei nº 9.430
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],

#Rule 91
# artigo 44, parágrafo 1º, da Lei 9.430
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}],

#Rule 92
# artigo 44, parágrafos 2º e 3º, da Lei 9.430
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN'}],

#Rule 93
# artigo 44, parágrafos 2º e 3º, da Lei nº 9.430
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],
    
#Rule 94
# artigo 44, parágrafos 2º e 3º, da Lei n. 9.430    
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'PROPN', 'OP': '?'}],

#Rule 95
# parágrafo 2º do artigo 5º da Lei 9.430    
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'lei'}, {}],
 
#Rule 96
# parágrafo 2º do artigo 5º da Lei nº 9.430/90
# parágrafo 2º do artigo 5º da Lei n. 9.430/90 
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'lei'}, {}, {'POS': 'NUM', 'OP': '?'}],
  
#Rule 97
# artigo 5º, parágrafo 1º, alínea "a" da Lei nº 9.430/90
# artigo 5º, parágrafo 1º, alínea a da Lei n. 9.430/90
# artigo 5º, parágrafo 1º, alínea A da Lei 1.234/90
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'lei'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NOUN', 'OP': '?'}, {}],   

#Rule 98
# art. 5º, § 1º, "a", da Lei nº 1.234/90
# art. 5º, § 1º, "a", da Lei n. 1.234/90
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'LOWER': 'lei'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NOUN', 'OP': '?'}, {}],
 
#Rule 99
# artigo 5º, § 1º, "a", da Lei 1.234/90
# artigo 5º, § 1º, "a", da Lei 1.234/1990
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'lei'}, {'POS': 'NUM'}],
    
#Rule 100
# artigo 5º, § 1º, alínea "a", da Lei 1.234/90
# artigo 5º, § 1º, alínea a, da Lei 1.234/90
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'lei'}, {'POS': 'NUM'}],

#Rule 101
# artigo 5º, § 1º, alínea a, da Lei nº 1.234/90
# artigo 5º, § 1º, alínea "a", da Lei nº 1.234/90
# artigo 5º, § 1º, alínea a, da Lei n. 1.234/90
# artigo 5º, § 1º, alínea "a", da Lei n. 1.234/90
# artigo 5º, § 1º, alínea "a", da Lei 1.234/90
# artigo 5º, § 1º, alínea a, da Lei 1.234/90
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'NUM'}],

#Rule 102
# § 1º, "a", do artigo 15 da Lei 1.234/90
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}],
 
#Rule 103
# § 1º, a, do artigo 15 da Lei n. 1.234/90
# § 1º, a, do artigo 15 da Lei nº 1.234/90
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM'}],

#Rule 104
# "a", § 1º, do artigo 15 da Lei 1.234/90
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {}],
    
#Rule 105
# "a", § 1º, do artigo 15 da Lei n. 1.234/90
# "a", § 1º, do artigo 15 da Lei nº 1.234/90
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM'}],   

# Rule 106
# artigo 5º, parágrafo 1º, "A", da Lei nº 9.430/90
# artigo 5º, parágrafo 1º, "A", da Lei 9.430/90
# artigo 5º, § 1º, "a", da Lei 1.234
# artigo 5º, § 1º, "a", da Lei nº 1.234
# artigo 5º, § 1º, "a", da Lei nº 1.234/90
# artigo 5º, § 1º, "a", da Lei nº 1.234/1990
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},  {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {}, {}],
 
# Rule 107
# artigo 5º, § 1º, alínea "a", da Lei n. 14.234/2000
# artigo 5º, § 1º, alínea "a", da Lei 14.234/2000
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP':'?'}, {}, {'LOWER': 'lei'}, {}, {}],

# Rule 108
# artigo 30 da Lei nº 9.784/99 Regra acima exige final com NUM, então essa foi necessária
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'lei'}, {'POS': 'NOUN'}, {'POS': 'PROPN'}],
    
# Rule 109
# artigos 1º e 2º da Lei nº 8.177/91
[{'LOWER': 'artigos'}, {}, {}, {}, {}, {'LOWER': 'lei'}, {}, {'POS': 'NUM'}],
    
]

# Rule 110
lista_lei = [
    [{'LOWER': 'lei'}, {'POS': 'NUM'}],
    [{'LOWER': 'lei'}, {'POS': 'PROPN'}],
    [{'LOWER': 'lei'}, {'POS': 'PROPN'}, {'POS': 'NUM'}],
    [{'LOWER': 'lei'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],
    [{'LOWER': 'lei'}, {'POS': 'NOUN'}, {'POS': 'NUM'}],   
]

# LISTA DOS PADRÕES - CÓDIGO CIVIL


lista_cod_civil = [
    
# Rule 01-CodCivil
# art. 9º do Código Civil
# art 9º do Código Civil
# art 15 do Código Civil
# art. 15 do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 02-CodCivil
# art. 9º do Codigo Civil
# art. 15 do Codigo Civil
# art. 15 do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],   

#Rule 03-CodCivil
# arts. 15 e 16 do Código Civil
# arts 15 e 16 do Código Civil
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 04-CodCivil
# arts 15 e 16 do Codigo Civil 
# arts 15 e 16 do Codigo Civil
# arts 15 e 16 do Codigo Civil
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
  
#Rule 05-CodCivil
# arts 15, 17 e 16 do Código Civil
# arts 15, 17, 16 do Código Civil
# arts. 15, 17, 16 do Código Civil
# arts. 15, 17 e 16 do Código Civil
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 06-CodCivil    
# arts. 15, 17 e 16 do Codigo Civil
# arts. 15, 17 e 16 do Codigo Civil
# arts. 15, 17, 16 do Codigo Civil
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 07-CodCivil
# art. 15, Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 08-CodCivil
# art. 15, Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 09-CodCivil
# inciso V do art. 15 do Código Civil
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 10-CodCivil
# inciso V do art. 15 do Codigo Civil 
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 11-CodCivil
# incisos II e V do art. 15 do Código Civil
[{'LOWER': 'incisos'}, {}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],    

#Rule 11-BBB-CodCivil
# incisos II e V do art. 15 do Codigo Civil
[{'LOWER': 'incisos'}, {}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
#Rule 12-CodCivil
# incisos II, V e VII do art. 15 do Código Civil
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 13-CodCivil
# incisos II, V e VII do art. 15 do Codigo Civil
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
#Rule 14-CodCivil   
# inciso I, do art. 165, do Código Civil
[{'LOWER': 'inciso'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
#Rule 15-CodCivil
# inciso I, do art. 15, do Codigo Civil
[{'LOWER': 'inciso'}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 16-CodCivil
# art. 44, inciso II, do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 17-CodCivil
# art. 44, inciso I, do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 18-CodCivil
# art. 44, incisos I e II, do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
#Rule 18-BBB-CodCivil
# art. 44, incisos I e II, do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 19-CodCivil
# art. 44, incisos I, II e III, do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP':'?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
 
#Rule 20-CodCivil
# art. 44, incisos I, II e III, do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP':'?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 21-CodCivil
# inc. V do art. 15 do Código Civil
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 22-CodCivil
# inc. V do art. 15 do Codigo Civil
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
#Rule 23-CodCivil
# incs. V e VII do art. 15 do Código Civil  
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
  
#Rule 24-CodCivil
# incs. V, VI e VII do art. 15 do Código Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},{}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 25-CodCivil
# incs. V e VII do art. 15 do Codigo Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
 
#Rule 26-CodCivil
# incs. V, VI e VII do art. 15 do Codigo Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},{}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 27-CodCivil
# arts. 2° e 13 da Lei Civil
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'PROPN', 'OP': '?'}, {}, {}, {'POS': 'ADP'}, {}, {'LOWER': 'lei'}, {'LOWER': 'civil'}],
    
#Rule 28-CodCivil
# art. 2° da Lei Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'lei'}, {'LOWER': 'civil'}],
    
#Rule 29-CodCivil
# § 1º do art. 21 do Código Civil
[{'ORTH': '§'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 30-CodCivil
# §§ 1º e 2º do art. 21 do Código Civil
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
#Rule 31-CodCivil
# § 1º do art. 21 do Codigo Civil
[{'ORTH': '§'}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
  
#Rule 32-CodCivil
# §§ 1º e 2º do art. 21 do Codigo Civil
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 33-CodCivil
# art. 21, § 2º, do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],    
   
#Rule 34-CodCivil
# art. 21, § 2º, do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
   
#Rule 35-CodCivil
# art. 21, §§ 2º e 3º, do Código Civil    
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}], 
 
#Rule 36-CodCivil
# art. 21, §§ 2º e 3º, do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
 
#Rule 37-CodCivil
# art. 44, parágrafo 1º, do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 38-CodCivil
# art. 44, parágrafo 1º, do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 39-CodCivil
# art. 44, parágrafos 2º e 3º, do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 40-CodCivil
# art. 44, parágrafos 2º e 3º, do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
#Rule 41-CodCivil
# art. 44, parágrafos 2º e 3º, da Lei Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'lei'}, {'LOWER': 'civil'}],
    
#Rule 42-CodCivil
# parágrafo 2º do art. 5º do Código Civil   
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
 
#Rule 43-CodCivil
# parágrafo 2º do art. 5º do Codigo Civil 
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
  
#Rule 44-CodCivil
# art. 5º, parágrafo 1º, alínea "a" do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],   

#Rule 44-BBB-CodCivil
# art. 5º, parágrafo 1º, alínea "a" do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
#Rule 45-CodCivil
# art. 5º, § 1º, "a", do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
 
#Rule 46-CodCivil
# art. 5º, § 1º, "a", do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
#Rule 47-CodCivil
# art. 5º, § 1º, alínea "a", do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'código'}, {'POS': 'civil'}],

#Rule 48-CodCivil
# art. 5º, § 1º, alínea a, do Codigo Civil
# art. 5º, § 1º, alínea "a", do Codigo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 49-CodCivil
# § 1º, "a", do art. 15 do Código Civil
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
 
#Rule 50-CodCivil
# § 1º, a, do art. 15 do Codigo Civil
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 51-CodCivil
# "a", § 1º, do art. 15 do Código Civil
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
#Rule 52-CodCivil
# "a", § 1º, do art. 15 do Codigo Civil
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],    
 
# Rule 53-CodCivil
# artigo 9º do Código Civil
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 54-CodCivil
# artigo 9º do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],   

#Rule 55-CodCivil
# artigos 15 e 16 do Código Civil
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 56-CodCivil
# artigos 15 e 16 do Codigo Civil
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
  
#Rule 57-CodCivil
# artigos 15, 17 e 16 do Código Civil
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 58-CodCivil
# artigos 15, 17 e 16 do Codigo Civil
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 59-CodCivil
# artigo 15, Código Civil
[{'LOWER': 'art'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 60-CodCivil
# artigo 15, Codigo Civil
[{'LOWER': 'artigo'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 61-CodCivil
# inciso V do artigo 15 do Código Civil
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 62-CodCivil
# inciso V do artigo 15 do Codigo Civil
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 63-CodCivil
# incisos II e V do artigo 15 do Código Civil
[{'LOWER': 'incisos'}, {}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],    

#Rule 64-CodCivil
# incisos II, V e VII do artigo 15 do Código Civil
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
#Rule 64-BBB-CodCivil
# incisos II, V e VII do artigo 15 do Codigo Civil
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
#Rule 65-CodCivil
# incisos II e VII do artigo 15 do Codigo Civil
[{'LOWER': 'incisos'}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 66-CodCivil
# inciso I, do artigo 165, do Código Civil
[{'LOWER': 'inciso'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
#Rule 67-CodCivil
# inciso I, do artigo 15, do Codigo Civil
[{'LOWER': 'inciso'}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 68-CodCivil
# artigo 44, inciso II, do Código Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 69-CodCivil
# artigo 44, inciso I, do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 70-CodCivil
# artigo 44, incisos I e II, do Código Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 71-CodCivil
# artigo 44, incisos I, II e III, do Código Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP':'?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
 
#Rule 72-CodCivil
# artigo 44, incisos II e III, do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 73-CodCivil
# artigo 44, incisos II, III e IV, do Codigo Civil 
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 74-CodCivil
# inc. V do artigo 15 do Código Civil
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 75-CodCivil
#inc. V do artigo 15 do Codigo Civil
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
# Rule 76-CodCivil
# incs. V e VII do artigo 15 do Código Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

# Rule 77-CodCivil
# incs. V, VI e VII do artigo 15 do Código Civi;
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

# Rule 77-BBB-CodCivil
# incs. V, VI e VII do artigo 15 do Codigo Civi;
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],    
    
# Rule 78-CodCivil
# incs. V e VII do artigo 15 do Codigo Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
# Rule 79-CodCivil
# artigos 2° e 13 da Lei Civil
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'PROPN', 'OP': '?'}, {}, {}, {'POS': 'ADP'}, {}, {'LOWER': 'lei'}, {'LOWER': 'civil'}],

# Rule 79-BBB-CodCivil
# artigo 2° do Código Civil
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

# Rule 80-CodCivil
# artigos 2º e 12 do Código Civil
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
# Rule 81-CodCivil
# artigos 2º, 5º e 12 do Código Civil Lembrar que em vários lugares há regras que terminam por capturar em duplicidade
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
#Rule 82-CodCivil
# § 1º do artigo 21 do Código Civil
[{'ORTH': '§'}, {}, {}, {'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 83-CodCivil
# §§ 1º e 2º do artigo 21 do Código Civil
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
#Rule 84-CodCivil
# § 1º do artigo 21 do Codigo Civil
[{'ORTH': '§'}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
  
#Rule 85-CodCivil
# §§ 1º e 2º do artigo 21 do Codigo Civil
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 86-CodCivil
# artigo 21, § 2º, do Código Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],    
   
#Rule 87-CodCivil
# artigo 21, § 2º, do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
   
#Rule 88-CodCivil
# artigo 21, §§ 2º e 3º, do Código Civil
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}], 
 
#Rule 89-CodCivil
# artigo 21, §§ 2º e 3º, do Codigo Civil
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
 
#Rule 90-CodCivil
# artigo 44, parágrafo 1º, do Código Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 91-CodCivil
# artigo 44, parágrafo 1º, do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 92-CodCivil
# artigo 44, parágrafos 2º e 3º, do Código Civil
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 93-CodCivil
# artigo 44, parágrafos 2º e 3º, do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
#Rule 94-CodCivil
# artigo 44, parágrafos 2º e 3º, do Código Civil   
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 95-CodCivil
# parágrafo 2º do artigo 5º do Código Civil   
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
 
#Rule 96-CodCivil
# parágrafo 2º do artigo 5º do Codigo Civil 
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
  
#Rule 97-CodCivil
# artigo 5º, parágrafo 1º, alínea "a" do Código Civil
# artigo 5º, parágrafo 1º, alínea a do Código Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],   

#Rule 97-BBB-CodCivil
# artigo 5º, parágrafo 1º, alínea "a" do Codigo Civil
# artigo 5º, parágrafo 1º, alínea a do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],   

#Rule 98-CodCivil
# art. 5º, § 1º, "a", do Código Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
 
#Rule 99-CodCivil
# artigo 5º, § 1º, "a", do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
    
#Rule 100-CodCivil
# artigo 5º, § 1º, alínea "a", do Código Civil
# artigo 5º, § 1º, alínea a, do Código Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

#Rule 101-CodCivil
# artigo 5º, § 1º, alínea a, do Codigo Civil
# artigo 5º, § 1º, alínea "a", do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 102-CodCivil
# § 1º, "a", do artigo 15 do Código Civil
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
 
#Rule 103-CodCivil
# § 1º, a, do artigo 15 do Codigo Civil
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],

#Rule 104-CodCivil
# "a", § 1º, do artigo 15 do Código Civil
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],
    
#Rule 105-CodCivil
# "a", § 1º, do artigo 15 do Codigo Civil
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],   

# Rule 106-CodCivil
# artigo 5º, parágrafo 1º, "A", do Código Civil
# artigo 5º, § 1º, "a", do Código Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},  {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

# Rule 106-BBB-CodCivil
# artigo 5º, parágrafo 1º, "A", do Codigo Civil
# artigo 5º, § 1º, "a", do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},  {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
        
# Rule 107-CodCivil
# artigo 5º, § 1º, alínea "a", do Código Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP':'?'}, {}, {'LOWER': 'código'}, {'LOWER': 'civil'}],

# Rule 107-CodCivil
# artigo 5º, § 1º, alínea "a", do Codigo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP':'?'}, {}, {'LOWER': 'codigo'}, {'LOWER': 'civil'}],
        
]

# LISTA DOS PADRÕES - CÓDIGO DE PROCESSO CIVIL


lista_cod_proc_civil = [
    
# Rule 01-CodPROCCivil
# art. 9º do novo Código de Processo Civil
# art 15 do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 02-CodPROCCivil
# art. 9º do novo Codigo de Processo Civil
# art. 15 do novo Codigo de Processo Civl
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
# Rule 02-ABREV-CodPROCCivil    
# art. 9º do CPC
# art. 9º do Novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],

#Rule 03-CodPROCCivil
# arts. 15 e 16 do novo Código de Processo Civil
# arts 15 e 16 do novo Código de Proceso Civil
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 04-CodPROCCivil
# arts 15 e 16 do novo Codigo de Processo Civil 
# arts. 15 e 16 do novo Codigo Processo Civil
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 04-ABREV-CodPROCCivil
# arts 15 e 16 do CPC 
# arts. 15 e 16 do novo CPC
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 05-CodPROCCivil
# arts 15, 17 e 16 do novo Código de Processo Civil
# arts. 15, 17, 16 do novo Código de Processo Civil
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 06-CodPROCCivil    
# arts. 15, 17 e 16 do novo Codigo de Processo Civil
# arts 15, 17, 16 do novo Codigo Processo Civil
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 06-ABREV-CodPROCCivil    
# arts. 15, 17 e 16 do novo CPC
# arts 15, 17, 16 do novo CPC
[{'LOWER': 'arts'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],

    
#Rule 07-CodPROCCivil
# art. 15, novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 08-CodPROCCivil
# art. 15, novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 08-ABREV-CodPROCCivil
# art. 15, novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],

#Rule 09-CodPROCCivil
# inciso V do art. 15 do novo Código de Processo Civil
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 10-CodPROCCivil
# inciso V do art. 15 do novo Codigo de Processo Civil 
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 10-ABREV-CodPROCCivil
# inciso V do art. 15 do novo CPC
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 11-CodPROCCivil
# incisos II e V do art. 15 do novo Código de Processo Civil
[{'LOWER': 'incisos'}, {}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],    

#Rule 11-BBB-CodPROCCivil
# incisos II e V do art. 15 do novo Codigo de Processo Civil
[{'LOWER': 'incisos'}, {}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 11-ABREV-CodPROCCivil
# incisos II e V do art. 15 do novo CPC
[{'LOWER': 'incisos'}, {}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    

#Rule 12-CodPROCCivil
# incisos II, V e VII do art. 15 do novo Código de Processo Civil
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 13-CodPROCCivil
# incisos II, V e VII do art. 15 do novo Codigo de Processo Civil
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 13-ABREV-CodPROCCivil
# incisos II, V e VII do art. 15 do novo CPC
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 14-CodPROCCivil   
# inciso I, do art. 165, do novo Código de Processo Civil
[{'LOWER': 'inciso'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 15-CodPROCCivil
# inciso I, do art. 15, do novo Codigo de Processo Civil
[{'LOWER': 'inciso'}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 15-ABREV-CodPROCCivil
# inciso I, do art. 15, do novo CPC
[{'LOWER': 'inciso'}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
        
#Rule 16-CodPROCCivil
# art. 44, inciso II, do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 17-CodPROCCivil
# art. 44, inciso I, do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 17-ABREV-CodPROCCivil
# art. 44, inciso I, do novo cpc
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 18-CodPROCCivil
# art. 44, incisos I e II, do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 18-BBB-CodPROCCivil
# art. 44, incisos I e II, do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 18-ABREV-BBB-CodPROCCivil
# art. 44, incisos I e II, do novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 19-CodPROCCivil
# art. 44, incisos I, II e III, do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP':'?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
 
#Rule 20-CodPROCCivil
# art. 44, incisos I, II e III, do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP':'?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 20-ABREV-CodPROCCivil
# art. 44, incisos I, II e III, do novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP':'?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
        
#Rule 21-CodPROCCivil
# inc. V do art. 15 do novo Código Processo Civil
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 22-CodPROCCivil
# inc. V do art. 15 do novo Codigo de Processo Civil
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 22-ABREV-CodPROCCivil
# inc. V do art. 15 do novo CPC
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 23-CodPROCCivil
# incs. V e VII do art. 15 do novo Código de Processo Civil  
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER':'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
  
#Rule 24-CodPROCCivil
# incs. V, VI e VII do art. 15 do novo Código de Processo Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},{}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 24-ABREV-CodPROCCivil
# incs. V, VI e VII do art. 15 do novo CPC
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},{}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 25-CodPROCCivil
# incs. V e VII do art. 15 do novo Codigo de Processo Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 25-ABREV-CodPROCCivil
# incs. V e VII do art. 15 do novo CPC
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
 
#Rule 26-CodPROCCivil
# incs. V, VI e VII do art. 15 do novo Codigo de Processo Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},{}, {}, {}, {'POS': 'ADP'}, {}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
        
#Rule 27-CodPROCCivil
# § 1º do art. 21 do novo Código de Processo Civil
[{'ORTH': '§'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 28-CodPROCCivil
# § 1º do art. 21 do novo Codigo de Processo Civil
[{'ORTH': '§'}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 28-ABREV-CodPROCCivil
# § 1º do art. 21 do novo CPC
[{'ORTH': '§'}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 29-CodPROCCivil
# §§ 1º e 2º do art. 21 do novo Código de Processo Civil
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 30-CodPROCCivil
# §§ 1º e 2º do art. 21 do novo Codigo de Processo Civil
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
      
#Rule 30-ABREV-CodPROCCivil
# §§ 1º e 2º do art. 21 do novo CPC
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],

#Rule 31-CodPROCCivil
# art. 21, § 2º, do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],    

#Rule 32-CodPROCCivil
# art. 21, § 2º, do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],    

#Rule 32-ABREV-CodPROCCivil
# art. 21, § 2º, do novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
       
#Rule 33-CodPROCCivil
# art. 21, §§ 2º e 3º, do novo Código de Processo Civil    
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}], 
 
#Rule 34-CodPROCCivil
# art. 21, §§ 2º e 3º, do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 34-ABREV-CodPROCCivil
# art. 21, §§ 2º e 3º, do novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
        
#Rule 35-CodPROCCivil
# art. 44, parágrafo 1º, do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 36-CodPROCCivil
# art. 44, parágrafo 1º, do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 36-ABREV-CodPROCCivil
# art. 44, parágrafo 1º, do novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
        
#Rule 37-CodPROCCivil
# art. 44, parágrafos 2º e 3º, do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 38-CodPROCCivil
# art. 44, parágrafos 2º e 3º, do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 38-ABREV-CodPROCCivil
# art. 44, parágrafos 2º e 3º, do novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
            
#Rule 39-CodPROCCivil
# parágrafo 2º do art. 5º do novo Código de Processo Civil   
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
 
#Rule 40-CodPROCCivil
# parágrafo 2º do art. 5º do novo Codigo de Proceso Civil 
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 40-ABREV-CodPROCCivil
# parágrafo 2º do art. 5º do novo Codigo de Proceso Civil 
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
        
#Rule 41-CodPROCCivil
# art. 5º, parágrafo 1º, alínea "a" do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],   

#Rule 42-BBB-CodPROCCivil
# art. 5º, parágrafo 1º, alínea "a" do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 42-ABREV-BBB-CodPROCCivil
# art. 5º, parágrafo 1º, alínea "a" do novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 43-CodPROCCivil
# art. 5º, § 1º, "a", do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
 
#Rule 44-CodPROCCivil
# art. 5º, § 1º, "a", do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 44-ABREV-CodPROCCivil
# art. 5º, § 1º, "a", do novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
        
#Rule 45-CodPROCCivil
# art. 5º, § 1º, alínea "a", do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'POS': 'civil'}],

#Rule 46-CodPROCCivil
# art. 5º, § 1º, alínea a, do novo Codigo de Processo Civil
# art. 5º, § 1º, alínea "a", do novo Codigo de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 46-ABREV-CodPROCCivil
# art. 5º, § 1º, alínea a, do novo CPC
# art. 5º, § 1º, alínea "a", do novo CPC
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
        
#Rule 47-CodPROCCivil
# § 1º, "a", do art. 15 do novo Código de Processo Civil
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
 
#Rule 48-CodPROCCivil
# § 1º, a, do art. 15 do novo Codigo de Processo Civil
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 48-ABREV-CodPROCCivil
# § 1º, a, do art. 15 do novo CPC
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
       
#Rule 49-CodPROCCivil
# "a", § 1º, do art. 15 do novo Código de Processo Civil
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 50-CodPROCCivil
# "a", § 1º, do art. 15 do novo Codigo de Processo Civil
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],    

#Rule 50-ABREV-CodPROCCivil
# "a", § 1º, do art. 15 do novo CPC
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
        
# Rule 51-CodPROCCivil
# artigo 9º do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 52-CodPROCCivil
# artigo 9º do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],   

#Rule 52-ABREV-CodPROCCivil
# artigo 9º do novo CPC
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],   

#Rule 53-CodPROCCivil
# artigos 15 e 16 do novo Código de Processo Civil
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 54-CodPROCCivil
# artigos 15 e 16 do novo Codigo de Processo Civil
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 54-ABREV-CodPROCCivil
# artigos 15 e 16 do novo CPC
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 55-CodPROCCivil
# artigos 15, 17 e 16 do novo Código de Processo Civil
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 56-CodPROCCivil
# artigos 15, 17 e 16 do novo Codigo de Processo Civil
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 56-ABREV-CodPROCCivil
# artigos 15, 17 e 16 do novo CPC
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True}, {}, {'IS_PUNCT': True, 'OP': '?'} , {'POS': 'CCONJ', 'OP': '?'},{}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 57-CodPROCCivil
# artigo 15, novo Código de Processo Civil
[{'LOWER': 'art'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 58-CodPROCCivil
# artigo 15, novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'},{'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 58-ABREV-CodPROCCivil
# artigo 15, novo CPC
[{'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'},{'LOWER': 'cpc'}],
        
#Rule 59-CodPROCCivil
# inciso V do artigo 15 do novo Código de Processo Civil
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 61-CodPROCCivil
# inciso V do artigo 15 do novo Codigo de Processo Civil
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 61-ABREV-CodPROCCivil
# inciso V do artigo 15 do novo CPC
[{'LOWER': 'inciso'}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 62-CodPROCCivil
# incisos II e V do artigo 15 do novo Código de Processo Civil
[{'LOWER': 'incisos'}, {}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],    

#Rule 63-CodPROCCivil
# incisos II, V e VII do artigo 15 do novo Código de Processo Civil
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 64-BBB-CodPROCCivil
# incisos II, V e VII do artigo 15 do novo Codigo de Processo Civil
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 65-CodPROCCivil
# incisos II e VII do artigo 15 do novo Codigo de Processo Civil
[{'LOWER': 'incisos'}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 64-ABREV-BBB-CodPROCCivil
# incisos II, V e VII do artigo 15 do novo CPC
[{'LOWER': 'incisos'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 65-ABREV-CodPROCCivil
# incisos II e VII do artigo 15 do novo CPC
[{'LOWER': 'incisos'}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
        
#Rule 66-CodPROCCivil
# inciso I, do artigo 165, do novo Código de Processo Civil
[{'LOWER': 'inciso'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 67-CodPROCCivil
# inciso I, do artigo 15, do novo Codigo de Processo Civil
[{'LOWER': 'inciso'}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 67-ABREV-CodPROCCivil
# inciso I, do artigo 15, do novo CPC
[{'LOWER': 'inciso'}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP':'?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 68-CodPROCCivil
# artigo 44, inciso II, do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 69-CodPROCCivil
# artigo 44, inciso I, do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 69-ABREV-CodPROCCivil
# artigo 44, inciso I, do novo CPC
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'inciso', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 70-CodPROCCivil
# artigo 44, incisos I e II, do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 71-CodPROCCivil
# artigo 44, incisos I, II e III, do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP':'?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
 
#Rule 72-CodPROCCivil
# artigo 44, incisos II e III, do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 73-CodPROCCivil
# artigo 44, incisos II, III e IV, do novo Codigo de Processo Civil 
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 72-ABREV-CodPROCCivil
# artigo 44, incisos II e III, do novo CPC
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],

#Rule 73-ABREV-CodPROCCivil
# artigo 44, incisos II, III e IV, do novo CPC
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'incisos', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],

#Rule 74-CodPROCCivil
# inc. V do artigo 15 do novo Código de Processo Civil
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {}, {'POS': 'NUM'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 75-CodPROCCivil
#inc. V do artigo 15 do novo Codigo de Processo Civil
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 75-ABREV-CodPROCCivil
#inc. V do artigo 15 do novo CPC
[{'LOWER': 'inc'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
# Rule 76-CodPROCCivil
# incs. V e VII do artigo 15 do novo Código de Processo Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

# Rule 77-CodPROCCivil
# incs. V, VI e VII do artigo 15 do novo Código de Processo Civil;
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

# Rule 77-BBB-CodPROCCivil
# incs. V, VI e VII do artigo 15 do novo Codigo de Processo Civil;
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],    
    
# Rule 78-CodPROCCivil
# incs. V e VII do artigo 15 do novo Codigo de Processo Civil
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

# Rule 77-ABREV-BBB-CodPROCCivil
# incs. V, VI e VII do artigo 15 do novo CPC
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
# Rule 78-ABREV-CodPROCCivil
# incs. V e VII do artigo 15 do novo CPC
[{'LOWER': 'incs'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
# Rule 79-BBB-CodPROCCivil
# artigo 2° do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

# Rule 80-CodPROCCivil
# artigos 2º e 12 do novo Código de Processo Civil
[{'LOWER': 'artigos'}, {}, {}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
# Rule 81-CodPROCCivil
# artigos 2º, 5º e 12 do novo Código de Processo Civil - Lembrar que em vários lugares há regras que terminam por capturar em duplicidade
[{'LOWER': 'artigos'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 82-CodPROCCivil
# § 1º do artigo 21 do novo Código de Processo Civil
[{'ORTH': '§'}, {}, {}, {'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 83-CodPROCCivil
# §§ 1º e 2º do artigo 21 do novo Código de Processo Civil
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 84-CodPROCCivil
# § 1º do artigo 21 do novo Codigo de Processo Civil
[{'ORTH': '§'}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
  
#Rule 85-CodPROCCivil
# §§ 1º e 2º do artigo 21 do novo Codigo de Processo Civil
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 84-ABREV-CodPROCCivil
# § 1º do artigo 21 do novo CPC
[{'ORTH': '§'}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
  
#Rule 85-ABREV-CodPROCCivil
# §§ 1º e 2º do artigo 21 do novo CPC
[{'ORTH': '§'}, {'ORTH': '§'}, {}, {}, {}, {}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 86-CodPROCCivil
# artigo 21, § 2º, do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],    
   
#Rule 87-CodPROCCivil
# artigo 21, § 2º, do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 87-ABREV-CodPROCCivil
# artigo 21, § 2º, do novo CPC
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 88-CodPROCCivil
# artigo 21, §§ 2º e 3º, do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}], 
 
#Rule 89-CodPROCCivil
# artigo 21, §§ 2º e 3º, do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 89-ABREV-CodPROCCivil
# artigo 21, §§ 2º e 3º, do novo CPC
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '$'}, {'ORTH': '$'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 90-CodPROCCivil
# artigo 44, parágrafo 1º, do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 91-CodPROCCivil
# artigo 44, parágrafo 1º, do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 91-ABREV-CodPROCCivil
# artigo 44, parágrafo 1º, do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 92-CodPROCCivil
# artigo 44, parágrafos 2º e 3º, do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 93-CodPROCCivil
# artigo 44, parágrafos 2º e 3º, do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 94-CodPROCCivil
# artigo 44, parágrafos 2º e 3º, do novo Código de Processo Civil   
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 94-ABREV-CodPROCCivil
# artigo 44, parágrafos 2º e 3º, do novo CPC  
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 95-CodPROCCivil
# parágrafo 2º do artigo 5º do novo Código de Processo Civil   
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
 
#Rule 96-CodPROCCivil
# parágrafo 2º do artigo 5º do novo Codigo de Processo Civil 
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 96-ABREV-CodPROCCivil
# parágrafo 2º do artigo 5º do novo CPC
[{'POS': 'NOUN'}, {}, {'POS': 'ADP'}, {'LOWER': 'artigo'}, {}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 97-CodPROCCivil
# artigo 5º, parágrafo 1º, alínea "a" do novo Código de Processo Civil
# artigo 5º, parágrafo 1º, alínea a do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'proceso'}, {'LOWER': 'civil'}],   

#Rule 97-BBB-CodCivil
# artigo 5º, parágrafo 1º, alínea "a" do novo Codigo de Processo Civil
# artigo 5º, parágrafo 1º, alínea a do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],   

#Rule 97-ABREV-BBB-CodCivil
# artigo 5º, parágrafo 1º, alínea "a" do novo CPC
# artigo 5º, parágrafo 1º, alínea a do novo CPC
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NOUN'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'} , {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],       
    
#Rule 98-CodPROCCivil
# art. 5º, § 1º, "a", do novo Código de Processo Civil
[{'LOWER': 'art'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
 
#Rule 99-CodPROCCivil
# artigo 5º, § 1º, "a", do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'},  {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 99-ABREV-CodPROCCivil
# artigo 5º, § 1º, "a", do novo CPC
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'},  {'LOWER': 'cpc'}],    
    
#Rule 100-CodPROCCivil
# artigo 5º, § 1º, alínea "a", do novo Código de Processo Civil
# artigo 5º, § 1º, alínea a, do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'ADV', 'OP': '?'}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 101-CodPROCCivil
# artigo 5º, § 1º, alínea a, do novo Codigo de Processo Civil
# artigo 5º, § 1º, alínea "a", do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 101-ABREV-CodPROCCivil
# artigo 5º, § 1º, alínea a, do novo CPC
# artigo 5º, § 1º, alínea "a", do novo CPC
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§', 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'alínea'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],
    
#Rule 102-CodPROCCivil
# § 1º, "a", do artigo 15 do novo Código de Processo Civil
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
 
#Rule 103-CodPROCCivil
# § 1º, a, do artigo 15 do novo Codigo de Processo Civil
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {},{'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

#Rule 103-ABREV-CodPROCCivil
# § 1º, a, do artigo 15 do novo CPC
[{'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {},{'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],    
    
#Rule 104-CodPROCCivil
# "a", § 1º, do artigo 15 do novo Código de Processo Civil
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],
    
#Rule 105-CodPROCCivil
# "a", § 1º, do artigo 15 do novo Codigo de Processo Civil
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],   

#Rule 105-ABREV-CodPROCCivil
# "a", § 1º, do artigo 15 do novo CPC
[{'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'artigo'}, {}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],   

# Rule 106-CodPROCCivil
# artigo 5º, parágrafo 1º, "A", do novo Código de Processo Civil
# artigo 5º, § 1º, "a", do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},  {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

# Rule 106-BBB-CodPROCCivil
# artigo 5º, parágrafo 1º, "A", do novo Codigo de Processo Civil
# artigo 5º, § 1º, "a", do  novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},  {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

# Rule 106-ABREV-BBB-CodPROCCivil
# artigo 5º, parágrafo 1º, "A", do novo CPC
# artigo 5º, § 1º, "a", do  novo CPC
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'},  {'IS_PUNCT': True, 'OP': '?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],

# Rule 107-CodPROCCivil
# artigo 5º, § 1º, alínea "a", do novo Código de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP':'?'}, {}, {'LOWER':'novo', 'OP': '?'}, {'LOWER': 'código'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

# Rule 107-CodPROCCivil
# artigo 5º, § 1º, alínea "a", do novo Codigo de Processo Civil
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP':'?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'codigo'}, {}, {'LOWER': 'processo'}, {'LOWER': 'civil'}],

# Rule 107-ABREV-CodPROCCivil
# artigo 5º, § 1º, alínea "a", do novo CPC
[{'LOWER': 'artigo'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'ORTH': '§'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_ALPHA': True}, {'IS_PUNCT': True, 'OP': '?'}, {'IS_PUNCT': True, 'OP':'?'}, {}, {'LOWER': 'novo', 'OP': '?'}, {'LOWER': 'cpc'}],

]

# CÓDIGO TRIBUTÁRIO NACIONAL
lista_ctn = [
            [{'LOWER': 'artigo'}, {'POS': 'NUM'}, {}, {'LOWER': 'código'}, {'LOWER': 'tributário'}, {}],
            [{'LOWER': 'art'}, {'POS': 'NUM'}, {}, {'LOWER': 'código'}, {'LOWER': 'tributário'}, {}],
            [{'LOWER': 'artigo'}, {'POS': 'NUM'}, {}, {'LOWER': 'ctn'}],
            [{'LOWER': 'art'}, {'POS': 'NUM'}, {}, {'LOWER': 'ctn'}]
]

lista_resp = [
    [{'LOWER': 'resp'}, {}, {'LIKE_NUM': True}],
    [{'LOWER': 'recurso'}, {'LOWER': 'especial'}, {}, {}, {'POS': 'NUM'}],
    [{'LOWER': 'recurso'}, {'LOWER': 'especial'}, {'POS': 'NUM'}],
    [{'LOWER': 'resp'}, {}, {}, {}, {}],
]

lista_recextraordinario = [
    [{'LOWER': 're'}, {}, {'LIKE_NUM': True}],
    [{'LOWER': 'recurso'}, {'LOWER': 'extraordinário'}, {}, {}, {'POS': 'NUM'}],
    [{'LOWER': 'recurso'}, {'LOWER': 'extraordinário'}, {'POS': 'NUM'}],
    [{'LOWER': 're'}, {}, {}, {}, {}],
]

matcher.add('Art Lei Geral', None, *lista_arts_lei_geral)
matcher.add('Artigo Lei Geral', None, *lista_artigos_lei_geral)   
matcher.add('Lei Geral', None, *lista_lei)
matcher.add('Artigo Código Civil', None, *lista_cod_civil)
matcher.add('Artigo CPC', None, *lista_cod_proc_civil)
matcher.add('CTN', None, *lista_ctn)
matcher.add('RE', None, *lista_recextraordinario)
matcher.add('REsp', None, *lista_resp)

