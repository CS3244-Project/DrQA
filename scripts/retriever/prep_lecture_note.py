import json

def preprocess(articles):
    articles = articles['data']
    doc = []
    for article in articles:
        for i,paragraph in enumerate(article['paragraphs']):
            text = paragraph['context']
            title = article['title'] +"_"+  str(i)
            doc.append((title,text))
    return doc

