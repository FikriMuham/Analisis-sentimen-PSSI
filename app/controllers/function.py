import re
# import pandas as pd
# import string
# import emoji
# import contractions
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text  import  CountVectorizer 

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.model_selection import  train_test_split
from  sklearn.svm  import  SVC
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import pickle
from sklearn.metrics import accuracy_score


factory = StemmerFactory()
stemmer = factory.create_stemmer()

f = open("app/controllers/stopword_list_tala.txt", "r")
isi = f.read()

tempStoplist = []
for tempstp in isi.split():
  tempStoplist.append(tempstp.lower())

cleantext = "(@[A-Za-z0-9_-]+)|([^A-Za-z \t\n])|(\w+:\/\/\S+)|(x[A-Za-z0-9]+)|(X[A-Za-z0-9]+)" #regex untuk remove punctuation
# Preprocessing
def preprocess_data(text):
  text = text.rstrip("\n")
  text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
  text = re.sub('RT\s', '', text)

  text = re.sub(cleantext,' ',str(text).lower()).strip() #casefolding dan remove punctuation
  # text = re.sub(r'[0-9]+', '', text, flags=re.MULTILINE)
  tokens = []
  for token in text.split():
    #if token in templist:
    if token not in tempStoplist: #jika token tidak di stopword maka simpan
      token = stemmer.stem(token) #lakukan stemming
      if len(token) >= 2:
      #if token != 'b':
        if token != 'rt':
          tokens.append(token) 
          text = " ".join(tokens)
  return text
  

# SVM
def result_svm(text):

  # text['label'] = text['label'].map({'positif': 2, 'negatif': 1, 'netral': 0})
  # x = text['Tweet'].fillna(' ')
  # y = text['label']
  # print (y)

  # vectorizer = TfidfVectorizer()
  # features = vectorizer.fit_transform(x)

  # pickle.dump(vectorizer, open('app/uploads/vectorizer.model','wb'))

  # x_train, x_test, y_train, y_test = train_test_split(features,y,test_size=0.5,random_state=2)


  # # Process of making models Klasifikasi SVM RBF
  # rbf = SVC(kernel="rbf", C=1.5, random_state=42)

  # rbf.fit(x_train,y_train)
  # y_rbf = rbf.predict(x_test)

  # pickle.dump(rbf, open('app/uploads/rbf.model','wb'))

  # accuracy = accuracy_score(y_test,  y_rbf)

    # Mengambil data teks dan label
  text['label'] = text['label'].map({'positif': 2, 'negatif': 1, 'netral': 0})
  X = text['Tweet'].fillna(' ')
  y = text['label']

  # Membagi data menjadi data latih dan data uji
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  # Membuat vektor fitur dengan CountVectorizer
  vectorizer = CountVectorizer()
  X_train_counts = vectorizer.fit_transform(X_train)

  # Melakukan transformasi TF-IDF pada vektor fitur
  tfidf_transformer = TfidfTransformer()
  X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

  # Melatih model Naive Bayes Multinomial
  model = MultinomialNB()
  model.fit(X_train_tfidf, y_train)

  # Menerapkan vektorisasi dan transformasi TF-IDF pada data uji
  X_test_counts = vectorizer.transform(X_test)
  X_test_tfidf = tfidf_transformer.transform(X_test_counts)

  # Melakukan prediksi pada data uji
  y_pred = model.predict(X_test_tfidf)

  # Menghitung akurasi
  accuracy = accuracy_score(y_test, y_pred)
  # print("Akurasi:", accuracy)

  return accuracy, y_test



  # clf_rbf.fit(x_train,y_train)
  # y_clf_rbf = clf_rbf.predict(x_test)
  # clfrakr  =  accuracy_score(y_test,  y_clf_rbf)
  # print("Training  accuracy  Score	:  ",clfr.score(x_train,y_train))
  # print("Vallidation  accuracy  Score	:  ",clfrakr  ) 
  # print("evaluasi rbf ", classification_report(y_test, y_clf_rbf),"\n")