# -*- coding: utf-8 -*-
"""MINetApplicationCode1_.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MRjoB9RA6pWlt12uToY9t6cKGbKxqNiU

# **App - Streamlit + Pycaret**
"""

import pycaret
from pycaret.regression import load_model, predict_model
import streamlit as st
import nltk
nltk.download('punkt')

from pycaret.classification import load_model
model = load_model('knn7')

def predict(model, input_df):
  predictions_df = predict_model(estimator=model, data=input_df)
  predictions = predictions_df['Label'][0]
  return predictions

def run():
  from PIL import Image
  image = Image.open('minetlogo.JPG')
  st.image(image, use_column_width = False)
  st.sidebar.info('MINet: A Novel Telemedicine Tool for Automagtically Assessing Motivational Interviewing (MI) Conversations Using Natural Language Processing')

import contractions

file_upload = st.file_uploader('Upload Transcript for Rating +  Feedback. Ensure they are in PDF/TXT form and the counselor and patient portions are indicated with "c:" and "p:" at the beginning of every line.', type=["txt","pdf"])
if file_upload is not None:
  file_contents2 = file_upload.read()
  fu = str(file_contents2)
  ru = contractions.fix(fu)
  yu = ru.lower()

  # preprocessing
  import nltk
  nltk.download('stopwords')
  from nltk.tokenize import word_tokenize  
  stopwords = nltk.corpus.stopwords.words('english')
  removed = ['c', ':', 't', '.', '?', '!', ',']
  stopwords.extend(removed)

  z = nltk.word_tokenize(yu)
  z2 = [word for word in z if word not in stopwords]

  nltk.download('wordnet')
  from nltk.corpus import wordnet
  nltk.download('averaged_perceptron_tagger')

  def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)
  from nltk.stem import WordNetLemmatizer

  lemmatizer = WordNetLemmatizer()
  for word in z2:
    qu = ((lemmatizer.lemmatize(word, get_wordnet_pos(word))))

  # word length
  wordcount3 = len(yu.split())


  if st.button("Predict"):
    print (wordcount3)
    """output = predict(model=model, input_df=input_df)
    if output==1:
      output="HIGH"
      st.success = ("Your MI conversations have a" + output + "quality")
    if output==0:
      output="LOW"
      st.success = ("Your MI conversations have a" + output + "quality")
  
  if st.button("Feedback"):
    if wordcount3 >= 1200:
      st.success = ("Your MI conversation needs to be longer, drawing out more of the complexities in patient's destructive habits.")
    if negativesentiment <= 0.5 and positivesentiment>=0.15 and neutralsentiment>=0.45:
      st.success = ("Your MI conversation needs to emphasize the more negative aspects of patient's problems - allow them to emphasize their emotions - try more open-ended questions. Ensure that you're not using excessive affirmations or reassurance.")
    if wordratio <= 10:
      st.success = ("Your MI conversation needs to include more input from you. While you need to ensure that your patients are describing their problems and feelings, you must also offer advice and reassurance.")
    if coherence_lda3 <= 0.265:
      st.success = ("Your MI conversation needs to make the topics of your conversation (specifically, the issues of the patient) more defined. Do not just offer general advice - cater your comments to the situation of the patient.")
    if jaccardsim <= 0.23:
      st.success = ("Your comments in the MI conversation needs to model the patient's word usage a little better. For example, if they say that drinking makes them feel less anxious, model their comments by saying 'So drinking makes you feel less anxious, and that's why you continue to do it.' Confirm their feelings.")


if __name__ == '__main__':
    run()
"""
