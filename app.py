# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 10:41:23 2025

@author: USER
"""

import streamlit as st
import pickle
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('punkt_tab')
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Email/Spam Classifier")

def transform_text(text):
    text= text.lower()
    text = nltk.word_tokenize(text)
    y=[]
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

input_sms = st.text_area('Enter the message')

if st.button("Predict"):
    #Preprocessing
    transformed_sms = transform_text(input_sms)
    
    #Vectorize
    vector_input = tfidf.transform([transformed_sms])
    
    #Predict
    result = model.predict(vector_input)[0]
    
    #Result
    if result==1:
        st.header("SPAM")
    else:
        st.header("NOT SPAM")
        
