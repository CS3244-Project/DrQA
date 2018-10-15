import json
import unidecode
def preprocess(articles):
    articles = articles['data']
    doc = []
    list_of_title =[]
    for article in articles:
        for i,paragraph in enumerate(article['paragraphs']):
            text = paragraph['context']
            title = unidecode.unidecode(article['title']) +"_"+  str(i)
            if title in list_of_title:
                title = title + "_2"
            else:
                list_of_title.append(title)
            doc.append((title,text))
    return doc

