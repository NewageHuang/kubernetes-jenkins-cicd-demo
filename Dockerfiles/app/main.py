# coding: utf-8

import numpy as np
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer

import itertools
import pickle
import scipy.sparse as sp
from flask import Flask, jsonify, request, app

# port number
web_port_number = 5002

# start the application
app = Flask(__name__)


# Lemma Tokenization

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


# subclass TfidfVectorizer
class MyVectorizer(TfidfVectorizer):
    # plug our pre-computed IDFs
    fname = "idf.npy"
    idfs = np.load(fname)
    TfidfVectorizer.idf_ = idfs


filename = 'finalized_model.sav'


# default home page & API instructions
@app.route('/')
def instruction():
    instruction = "<br>This is kubernetes jenkins CI/CD demo.</br>"
    return instruction


@app.route('/detector', methods=['POST'])
def detector_api():
    text = request.get_data()
    # loading saved idf and vocabulary
    idfs = np.load("idf.npy")
    with open('vocab.pkl', 'rb') as fp:
        u = pickle._Unpickler(fp)
        u.encoding = 'latin1'
        vocab = u.load()

    # instantiate vectorizer
    vectorizer = MyVectorizer(stop_words='english', max_df=0.66, tokenizer=LemmaTokenizer())

    # plug _tfidf._idf_diag
    vectorizer._tfidf._idf_diag = sp.spdiags(idfs, diags=0, m=len(idfs), n=len(idfs))
    vectorizer.vocabulary_ = vocab

    vec = vectorizer.transform([text])
    with open(filename, 'rb') as fp:
        u = pickle._Unpickler(fp)
        u.encoding = 'latin1'
        loaded_model = u.load()
    result = loaded_model.predict(vec)
    return jsonify([result[0].decode('UTF-8')])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=web_port_number, debug=True)
