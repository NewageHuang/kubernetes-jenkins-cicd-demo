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

# default home page & API instructions
@app.route('/')
def instruction():
    instruction = "<br>This is kubernetes jenkins CI/CD demo.</br>"
    return instruction

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=web_port_number, debug=True)
