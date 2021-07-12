import pycaret
from pycaret.regression import load_model, predict_model
import streamlit as st

from pycaret.classification import load_model
model = load_model('/knn7')

def predict(model, input_df):
  predictions_df = predict_model(estimator=model, data=input_df)
  predictions = predictions_df['Label'][0]
  return predictions

def run():
  from PIL import Image
  image = Image.open('/content/drive/MyDrive/minetlogo.JPG')
  st.image(image,use_column_width = False)
  st.sidebar.info('MINet: A Novel Telemedicine Tool for Automatically Assessing Motivational Interviewing (MI) Conversations Using Natural Language Processing')

file_upload = st.file_uploader('Upload Transcript for Rating +  Feedback. Ensure they are in PDF/TXT form and th counselor and patient portions are indicated with "c:" and "p:" at the beginning of every line.', type=["txt","pdf"])
if file_upload is not None:
  fu = open(item, 'file_upload')
  file_contents2 = file_upload.read()
  fu.close()
  ru = contractions.fix(file_contents2)
  yu = ru.lower()

  # preprocessing
  import nltk
  nltk.download('stopwords')
  from nltk.tokenize import word_tokenize  
  stopwords = nltk.corpus.stopwords.words('english')
  removed = ['c', ':', 't', '.', '?', '!', ',']
  stopwords.extend(removed)

  z = nltk.work_tokenize(yu)
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

  lemmatizer = WordNetLemmatizer()
  for word in z2:
    qu = ((lemmatizer.lemmatize(word, get_wordnet_pos(word))))

  # word length
  wordcount3 = len(yu.split())

  # sentiment
  import stanza
  import itertools
  print("Downloading English model...")
  stanza.download('en')
  print("Building an English pipeline...")
  en_nlp = stanza.Pipeline('en')
  lines3 = yu.splitlines()
  for item in lines3:
    sentiment3 = []
    doc = en_nlp(item)
    for i, sentence in enumerate(doc.sentences):
      ruu=sentence.sentiment
      sentiment3.append(ruu)
    sentiment.append(sentiment3)
  from collections import Counter 
  sentimentdict = []
  merged = list(itertools.chain(*sentiment))
  a = Counter(merged)
  b= dict(a) 
  searchkey1 = 0
  searchkey2 = 1
  searchkey3 = 2
  if searchkey1 in b.keys():
    negativesentiment = ((b[0])/(len(item)))
  else:
    negativesentiment = (0)
  if searchkey2 in b.keys():
    neutralsentiment = ((b[1])/(len(item)))
  else:
    neutralsentiment = (0)
  if searchkey3 in b.keys():
    positivesentiment = ((b[2])/(len(item)))
  else:
    positivesentiment = (0)


  # counselor-patient word ratios
  lines4 = yu.splitlines()
  counselorsq =[]
  patientsq = []
  for item in lines4:
    if item.startsiwth("c: "):
      counselorsq.append(item)
    if item.startswith("p: "):
      patientsq.append(item)
  for item in counselorsq:
    counselorwordcount = len(item.split())
    patientwordcount = len(item.split())
  counselortopatientratio = counselorwordcount/patientwordcount

  # jaccard similarity
  def get_jaccard_sim(str1, str2): 
    a = set(str1.split()) 
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))
  
  for item in counselorsq:
    counselor = item
  for item in patientsq:
    patient = item
  jaccardsim = get_jaccard_sim(counselor, patient)

  # lda topic vectors
  topicqu = []
  topicqu.append(qu)
  train_vecs = []
  from gensim import corpora, models
  dictionary_LDA3 = corpora.Dictionary(topicqu)
  corpus = [dictionary_LDA3.doc2bow(list_of_tokens) for list_of_tokens in topicqu]
  num_topics = 5
  lda_model3 = models.LdaModel(corpus, num_topics=num_topics, \
                               id2word=dictionary_LDA3, \
                               passes=4, alpha=[0.01]*num_topics, \
                               eta=[0.01]*len(dictionary_LDA3.keys()))
  
  from gensim.models import CoherenceModel
  # Compute Coherence Score
  coherence_model_lda3 = CoherenceModel(model=lda_model3, texts=topicqu, dictionary=dictionary_LDA3, coherence='c_v')
  coherence_lda3 = coherence_model_lda3.get_coherence()

  train_vecs4 = []
  from gensim import corpora, models
  ID2word4 = corpora.Dictionary(topicqu)

  train_corpus = [ID2word4.doc2bow(doc) for doc in topicqu]

  for i in range(len(topicqu)):
    top_topics4 = lda_model3.get_document_topics(train_corpus4, minimum_probability=0.0)
    topic_vec4 = [top_topics[i][1] for i in range(7)]
    train_vecs4.append(topic_vec4)

  input_dict = {'Word Count': wordcount3,
                 'Negative Sentiment Frequency': negativesentiment,
                 'Neutral Sentiment Frequency': neutralsentiment,
                 'Positive Sentiment Frequency': positivesentiment,
                 'Counselor-to-Patient Word Ratio': wordratio,
                 'Topics': ldawordvecs,
                 'Word Usage Similarity': jaccardsim,
                 'Labels': labels}
  input_df = pd.DataFrame([input_dict])

  if st.button("Predict"):
    output = predict(model=model, input_df=input_df)
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
