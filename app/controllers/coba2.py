from app import app

from app.controllers.coba import preprocess_data, tfidf_transformer, bow_transformer
import joblib




# Load model dari file
model = joblib.load("twitter_sentiment.pkl")

# Contoh teks yang ingin diprediksi
new_text = "pssi kinerja nya baik"

# Lakukan preprocessing pada teks baru
preprocessed_text = preprocess_data(new_text)

# Transformasikan teks baru menjadi vektor TF-IDF menggunakan vectorizer yang sama
vectorized_text = tfidf_transformer.transform(bow_transformer.transform([preprocessed_text]))

# Lakukan prediksi menggunakan model
prediction = model.predict(vectorized_text)

# Mengubah label hasil prediksi menjadi label yang lebih bermakna (misalnya "positif", "negatif", "netral")
if prediction == 0:
    label = "netral"
elif prediction == 1:
    label = "negatif"
else:
    label = "positif"

# Menampilkan hasil prediksi
print("Hasil prediksi:", label)
