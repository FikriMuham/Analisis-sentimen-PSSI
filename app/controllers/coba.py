import pandas as pd
import numpy as np
import re
import emoji
import contractions
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import joblib

import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# Membaca data dari file CSV
# df = pd.read_csv('D:\KULIAH POLTEK_HARBER\Semester\Semester 8\TA\Cutbox\app\uploads\label_manual (1).csv', usecols=['tweet','label'] )
df = pd.read_csv('D:\\KULIAH POLTEK_HARBER\\Semester\\Semester 8\\TA\\Cutbox\\app\\uploads\\label_manual (1).csv', usecols=['tweet','label'])

def preprocess_data(tweet):
# def cleansing(tweet):
    # Replace RT tag
    t1 = re.sub('RT\s', '', tweet)
    # Replace @_username
    t2 = re.sub('\B@\w+', "", t1)
    # Replace emojis with text
    t3 = emoji.demojize(t2)
    # Replace URL (http:// or https://)
    t4 = re.sub('(http|https):\/\/\S+', '', t3)
    # Replace #_something_
    t5 = re.sub('#+', '', t4)
    # Lower case each letter
    t6 = t5.lower()
    # Replace word repetition with a single occurrence ('ooooooooo' becomes 'oo')
    t7 = re.sub(r'(.)\1+', r'\1\1', t6)
    # Replace punctuation repetition with a single occurrence ('!!!!!!!!' becomes '!')
    t8 = re.sub(r'[\?\.\!]+(?=[\?.\!])', '', t7)
    # Alphabets only, exclude numbers and special characters
    t9 = re.sub(r'[^a-zA-Z]', ' ', t8)
    # Replace contractions with their extended forms
    t10 = contractions.fix(t9)
    return t10

# Contoh penggunaan cleansing pada setiap tweet dalam DataFrame
for i, r in df.iterrows():
    y = preprocess_data(r['tweet'])
    df.loc[i, 'tweet'] = y

# Drop duplicates based on the 'tweet' column
df = df.drop_duplicates('tweet')

# Initialize Sastrawi stemmer and stopword remover
stemmer = StemmerFactory().create_stemmer()
stopword_remover = StopWordRemoverFactory().create_stop_word_remover()

# Tokenize helper function
def text_process(raw_text):
    # Remove punctuation
    nopunc = ''.join([char for char in raw_text if char not in string.punctuation])

    # Remove stopwords and stem the words
    processed_text = ' '.join([stemmer.stem(word) for word in stopword_remover.remove(nopunc).split()])

    return processed_text

# Create a new column 'tokens' with processed text
df['tokens'] = df['tweet'].apply(text_process)

# # Create an empty list to store all words
# all_words = []

# # Iterate over each line in the 'tokens' column of the DataFrame
# for line in df['tokens']:
#     # Extend the list with words in the line
#     all_words.extend(line)

# # Create a word frequency dictionary
# wordfreq = Counter(all_words)

# Membuat CountVectorizer dan melatihnya dengan teks yang telah di-preprocess
bow_transformer = CountVectorizer(analyzer=text_process).fit(df['tweet'])

# Contoh teks yang telah divectorize
sample_tweet = df['tweet'][0]

# Representasi vektor
bow_sample = bow_transformer.transform([sample_tweet])

# Transformasi seluruh DataFrame of messages menjadi representasi vektor
messages_bow = bow_transformer.transform(df['tweet'])

# Membuat dan melatih TfidfTransformer dengan vektor dari CountVectorizer
tfidf_transformer = TfidfTransformer().fit(messages_bow)

# Melakukan transformasi TF-IDF pada contoh vektor bow_sample
tfidf_sample = tfidf_transformer.transform(bow_sample)

# Melakukan transformasi TF-IDF pada seluruh bag-of-words corpus
messages_tfidf = tfidf_transformer.transform(messages_bow)

# Membuat train-test split
X_train, X_test, y_train, y_test = train_test_split(df['tweet'], df['label'], test_size=0.2, random_state=123)

# Membuat pipeline
pipeline = Pipeline([
    ('bow', CountVectorizer(strip_accents='ascii', lowercase=True)),
    ('tfidf', TfidfTransformer()),
    ('classifier', MultinomialNB())
])

# Mendefinisikan parameter untuk GridSearchCV
parameters = {
    'bow__ngram_range': [(1, 1), (1, 2)],
    'tfidf__use_idf': (True, False),
    'classifier__alpha': (1e-2, 1e-3),
}

# Melakukan GridSearchCV
grid = GridSearchCV(pipeline, cv=10, param_grid=parameters, verbose=1)
grid.fit(X_train, y_train)

# # Menampilkan hasil terbaik dari GridSearchCV
# print("\nBest Model: %f using %s" % (grid.best_score_, grid.best_params_))
# print('\n')

# Evaluasi model
means = grid.cv_results_['mean_test_score']
stds = grid.cv_results_['std_test_score']
params = grid.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("Mean: %f Stdev:(%f) with: %r" % (mean, stdev, param))

# Menyimpan model terbaik
joblib.dump(grid, "twitter_sentiment.pkl")

# Meload model dari file
model_NB = joblib.load("twitter_sentiment.pkl")

# Memprediksi dengan model terbaik
y_preds = model_NB.predict(X_test)

# Menampilkan metrik evaluasi
print('Accuracy score:', accuracy_score(y_test, y_preds))
print('\n')
print('Confusion matrix:\n', confusion_matrix(y_test, y_preds))
print('\n')
print(classification_report(y_test, y_preds))

