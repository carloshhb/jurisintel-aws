import pt_core_news_sm

nlp = pt_core_news_sm.load()

dict_jus = list()

with open('pickle.txt') as f:
    dict_jus.append(f.readline())

dicio_juris = []
for item in dict_jus:
    dicio_juris.append(item)

dicio_juris_nlp = []

for item in dicio_juris:
    txt_nlp = nlp(item)
    if len(txt_nlp) < 10:
        dicio_juris_nlp.append(txt_nlp)
