#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import re
from string import punctuation
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentimientos.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def generarStopWords():
    nltk.download('stopwords')
    nltk.download('wordnet') 
    ##Creating a list of stop words and adding custom stopwords
    stop_words = set(stopwords.words('spanish'))
    ##Creating a list of custom stopwords
    new_words = ["de", "la", "que", "el", "en", "y", 
                 "a", "los", "del", "se", "las", "por", 
                 "un", "para", "con", "no", "una", "su", 
                 "al", "lo", "como", "más", "pero", "sus", 
                 "le", "ya", "o", "este", "sí", "porque", 
                 "esta", "entre", "cuando", "muy", "sin", 
                 "sobre", "también", "me", "hasta", "hay", 
                 "donde", "quien", "desde", "todo", "nos", 
                 "durante", "todos", "uno", "les", "ni", 
                 "contra", "otros", "ese", "eso", "ante", 
                 "ellos", "e", "esto", "mí", "antes", "algunos", 
                 "qué", "unos", "yo", "otro", "otras", "otra", "él", 
                 "tanto", "esa", "estos", "mucho", "quienes", "nada", 
                 "muchos", "cual", "poco", "ella", "estar", "estas", 
                 "algunas", "algo", "nosotros", "mi", "mis", "tú", 
                 "te", "ti", "tu", "tus", "ellas", "nosotras", 
                 "vosotros", "vosotras", "os", "mío", "mía", "míos", 
                 "mías", "tuyo", "tuya", "tuyos", "tuyas", "suyo", 
                 "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", 
                 "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos", 
                 "esas", "estoy", "estás", "está", "estamos", "estáis", "están", 
                 "esté", "estés", "estemos", "estéis", "estén", "estaré", "estarás", 
                 "estará", "estaremos", "estaréis", "estarán", "estaría", "estarías", 
                 "estaríamos", "estaríais", "estarían", "estaba", "estabas", "estábamos", 
                 "estabais", "estaban", "estuve", "estuviste", "estuvo", "estuvimos", 
                 "estuvisteis", "estuvieron", "estuviera", "estuvieras", "estuviéramos", 
                 "estuvierais", "estuvieran", "estuviese", "estuvieses", "estuviésemos", 
                 "estuvieseis", "estuviesen", "estando", "estado", "estada", "estados", 
                 "estadas", "estad", "he", "has", "ha", "hemos", "habéis", "han", "haya", 
                 "hayas", "hayamos", "hayáis", "hayan", "había", "habías", "habíamos", 
                 "habíais", "habían", "hube", "hubiste", "hubo", "hubimos" ]

    stop_words = stop_words.union(new_words)
    return stop_words
stop = generarStopWords()
def preprocess_df(dataframe):
    dataframe['COMENTARIO'] = dataframe['COMENTARIO'].apply(preprocessor)
    return dataframe
def tokenize_comments(dataframe_entrada):
    max_features = 250
    tokenizer = Tokenizer(num_words=max_features, split=' ')
    tokenizer.fit_on_texts(dataframe_entrada['COMENTARIO'].values)
    X = tokenizer.texts_to_sequences(dataframe_entrada['COMENTARIO'].values)
#     maxlen = max(len(seq) for seq in X)
    X = pad_sequences(X, maxlen=82)
    return X
def preprocessor(text):#tokenizer
    #text = re.sub('[^a-zA-z0-9ñ\s]','',text)
    text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text) #remove tags
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')
    
    #Corrección ortografía
    
    text = normalize(text)
    
    text = ''.join([c if c not in punctuation else ' '+c+' ' \
                    for c in text]).lower()    
    #text=re.sub("(\\d|\\W)+"," ",text) # remove special characters and digits
    ##Stemming
    text = text.split()
    #ps=PorterStemmer()
    #Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in  
            stop]
    
    tokenized = " ".join(text)
    return tokenized
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("à", "a"),
        ("è", "e"),
        ("ì", "i"),
        ("ò", "o"),
        ("ù", "u"),
        #("ñ", "n"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

if __name__ == '__main__':
    main()
