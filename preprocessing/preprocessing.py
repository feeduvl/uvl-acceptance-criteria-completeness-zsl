import string

import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

nltk.download('punkt')

def full_preprocessing(doc_text):
    """ Perform full preprocessing on a string """
    if not isinstance(doc_text, str):
        raise TypeError
    doc_text = remove_punctuation(doc_text)
    token_list = get_tokenized_list(doc_text)
    token_list = remove_stopwords(token_list)
    token_list = word_stemmer(token_list)
    output = ' '.join(token_list)
    return output


def get_tokenized_list(doc_text):
    """ Converts a string into a tokenized list """
    return word_tokenize(doc_text)


def word_stemmer(token_list):
    """ Performs stemming on a tokenized list """
    if not isinstance(token_list, list):
        raise TypeError
    ps = PorterStemmer()
    stemmed = []
    for words in token_list:
        stemmed.append(ps.stem(words))
    return stemmed



def remove_stopwords(token_list):
    """ Perform stop word removal on a tokenized list """
    if not isinstance(token_list, list):
        raise TypeError
    cleaned_token_list = []
    for word in token_list:
        if word.lower() not in ENGLISH_STOP_WORDS:
            cleaned_token_list.append(word)
    return cleaned_token_list


def remove_punctuation(doc_text: str):
    """ Perform punctuation removal on a string """
    return doc_text.translate(str.maketrans('', '', string.punctuation))
