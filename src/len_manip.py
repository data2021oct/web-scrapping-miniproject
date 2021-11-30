from googletrans import Translator

import spacy
import re
from textblob import TextBlob
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer




nlp = spacy.load("en_core_web_sm")
stop = nlp.Defaults.stop_words






def english(col):
    """
    recibe un string
    lo traduce al inglés
 
    """
    trans = Translator()
    try:    
        trad = trans.translate(col,dest="en")
        return trad.text
    except:
        return col
    
def tokenizer (txt):
    """
    recibe un texto
    lo devuelve tokenizado *explicar mejor
    
    """    
    tokens = nlp(txt)
    filtradas = []
    for token in tokens:
        if not token.is_stop:
            lemma = token.lemma_.lower().strip()
            if re.search('^[a-zA-Z]+$',lemma): # Esto me quita las interrogaciones
                filtradas.append(lemma)
    return " ".join(filtradas)

def sentimental(col):
    """
    recibe un texto
    devuelve una lista con los indicadores de sentiments:
    [polaridad,subjetividad,negatividad,neutralidad,positividad, media de las ultimas tres]
    """
    total = []
    
    blob = TextBlob(col)
    total.append(blob.sentiment[0])
    total.append(blob.sentiment[1])
    
    sia = SentimentIntensityAnalyzer()
    polaridad = sia.polarity_scores(col)
    total.append(polaridad["neg"])
    total.append(polaridad["neu"])
    total.append(polaridad["pos"])
    total.append(polaridad["compound"])
    return total

def cuentastok(col):
    """
    recibe un string (pensado para dataframes)
    cuenta las palabras de este string
    devuelve un lista con la cuenta(s)
    """
    tot = []
    for c in col:
        tot.append(len(c.split(" ")))
    return sum(tot)