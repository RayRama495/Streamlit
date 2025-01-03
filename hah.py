# -*- coding: utf-8 -*-
"""hah.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NJ-DT1cG9nMWmspEs1LrhyqgOaUzpi5L
"""

import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

file_path = ('water_potability.csv')
water_data = pd.read_csv(file_path)

water_data.head()

df=water_data.copy()

print ("Jumlah baris : ",water_data.shape[0])

water_data.dtypes

water_data.nunique()

water_data.isnull().sum()

# Menghitung Z-Score
z_scores = stats.zscore(df.select_dtypes(include=['float64', 'int64']))

# Menentukan batas Z-Score (misalnya > 3 atau < -3)
outliers_zscore = (z_scores > 3) | (z_scores < -3)

# Menampilkan jumlah outlier per kolom
print("Jumlah outlier berdasarkan Z-Score:")
print(outliers_zscore.sum())

numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
df[numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].mean())

# Memeriksa apakah masih ada missing values setelah imputasi
missing_values_after = df.isnull().sum()
print("\nJumlah missing values setelah imputasi rata-rata:")
print(missing_values_after)

# Memeriksa apakah masih ada missing values
if df.isnull().sum().sum() == 0:
    print("\nImputasi berhasil, tidak ada missing values yang tersisa.")
else:
    print("\nMasih ada missing values setelah imputasi.")

from imblearn.over_sampling import SMOTE

# Memisahkan fitur (X) dan target (y)
X = df.drop('Potability', axis=1)
y = df['Potability']

# Menggunakan SMOTE untuk oversampling kelas minoritas
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Menyusun ulang DataFrame setelah resampling
df_resampled = pd.DataFrame(X_resampled, columns=X.columns)
df_resampled['Potability'] = y_resampled

# Visualisasi distribusi 'Potability' setelah resampling
plt.figure(figsize=(8, 6))
sns.countplot(x='Potability', data=df_resampled)
plt.title('Distribusi Potability Setelah Resampling')
plt.xlabel('Potability (0 = Tidak Dapat Diminum, 1 = Dapat Diminum)')
plt.ylabel('Jumlah')
plt.show()

# Membuat plot untuk membandingkan distribusi sebelum dan setelah resampling
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Sebelum resampling
sns.countplot(x='Potability', data=df, ax=axes[0])
axes[0].set_title('Distribusi Potability Sebelum Resampling')
axes[0].set_xlabel('Potability (0 = Tidak Dapat Diminum, 1 = Dapat Diminum)')
axes[0].set_ylabel('Jumlah')

# Setelah resampling
sns.countplot(x='Potability', data=df_resampled, ax=axes[1])
axes[1].set_title('Distribusi Potability Setelah Resampling')
axes[1].set_xlabel('Potability (0 = Tidak Dapat Diminum, 1 = Dapat Diminum)')
axes[1].set_ylabel('Jumlah')

plt.tight_layout()
plt.show()

# Menghitung korelasi antar kolom numerik
correlation_matrix = df.corr()

# Membuat heatmap untuk visualisasi korelasi antar atribut
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
plt.title('Korelasi Antar Atribut')
plt.show()

# Membagi menjadi dua bagian
set_1 = numerical_columns[:5]
set_2 = numerical_columns[5:]

# Set 1
plt.figure(figsize=(15, 12))
for i, col in enumerate(set_1, 1):
    plt.subplot(2, 3, i)
    sns.histplot(df[col], kde=True, bins=20)
    plt.title(f'Distribusi {col}')

plt.tight_layout()
plt.show()

# Set 2
plt.figure(figsize=(15, 12))
for i, col in enumerate(set_2, 1):
    plt.subplot(2, 3, i)
    sns.histplot(df[col], kde=True, bins=20)
    plt.title(f'Distribusi {col}')

plt.tight_layout()
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

# Membuat model Gaussian Naive Bayes
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# Prediksi dan evaluasi model
y_pred_gnb = gnb.predict(X_test)
accuracy_gnb = accuracy_score(y_test, y_pred_gnb)
conf_matrix_gnb = confusion_matrix(y_test, y_pred_gnb)

print(f"Akurasi Gaussian Naive Bayes: {accuracy_gnb:.4f}")
print("Confusion Matrix Gaussian Naive Bayes:")
print(conf_matrix_gnb)

# Membuat model Decision Tree
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

# Prediksi dan evaluasi model
y_pred_dt = dt.predict(X_test)
accuracy_dt = accuracy_score(y_test, y_pred_dt)
conf_matrix_dt = confusion_matrix(y_test, y_pred_dt)

print(f"Akurasi Decision Tree: {accuracy_dt:.4f}")
print("Confusion Matrix Decision Tree:")
print(conf_matrix_dt)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred_knn = knn.predict(X_test)
accuracy_knn = accuracy_score(y_test, y_pred_knn)
conf_matrix_knn = confusion_matrix(y_test, y_pred_knn)

print(f"Akurasi K-Nearest Neighbors: {accuracy_knn:.4f}")
print("Confusion Matrix K-Nearest Neighbors:")
print(conf_matrix_knn)

import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

sns.heatmap(conf_matrix_gnb, annot=True, fmt='d', cmap='Blues', ax=axes[0])
axes[0].set_title('Confusion Matrix Gaussian Naive Bayes')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('Actual')

sns.heatmap(conf_matrix_dt, annot=True, fmt='d', cmap='Blues', ax=axes[1])
axes[1].set_title('Confusion Matrix Decision Tree')
axes[1].set_xlabel('Predicted')
axes[1].set_ylabel('Actual')

sns.heatmap(conf_matrix_knn, annot=True, fmt='d', cmap='Blues', ax=axes[2])
axes[2].set_title('Confusion Matrix K-Nearest Neighbors')
axes[2].set_xlabel('Predicted')
axes[2].set_ylabel('Actual')

plt.tight_layout()
plt.show()

# Misalnya, X adalah fitur dan y adalah target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Tanpa normalisasi (Model asli)
# Inisialisasi model
gnb = GaussianNB()
dt = DecisionTreeClassifier(random_state=42)
knn = KNeighborsClassifier(n_neighbors=5)

# Latih dan evaluasi model tanpa normalisasi
gnb.fit(X_train, y_train)
dt.fit(X_train, y_train)
knn.fit(X_train, y_train)

# Prediksi dan hitung akurasi
gnb_acc = accuracy_score(y_test, gnb.predict(X_test))
dt_acc = accuracy_score(y_test, dt.predict(X_test))
knn_acc = accuracy_score(y_test, knn.predict(X_test))

print(f"Akurasi GaussianNB tanpa normalisasi: {gnb_acc:.4f}")
print(f"Akurasi Decision Tree tanpa normalisasi: {dt_acc:.4f}")
print(f"Akurasi KNN tanpa normalisasi: {knn_acc:.4f}")
print("")

# Dengan normalisasi (menggunakan StandardScaler)
scaler = StandardScaler()

# Terapkan normalisasi pada data latih dan uji
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Latih dan evaluasi model dengan normalisasi
gnb.fit(X_train_scaled, y_train)
dt.fit(X_train_scaled, y_train)
knn.fit(X_train_scaled, y_train)

# Prediksi dan hitung akurasi setelah normalisasi
gnb_scaled_acc = accuracy_score(y_test, gnb.predict(X_test_scaled))
dt_scaled_acc = accuracy_score(y_test, dt.predict(X_test_scaled))
knn_scaled_acc = accuracy_score(y_test, knn.predict(X_test_scaled))

print(f"Akurasi GaussianNB setelah di normalisasi: {gnb_scaled_acc:.4f}")
print(f"Akurasi Decision Tree setelah di normalisasi: {dt_scaled_acc:.4f}")
print(f"Akurasi KNN setelah di normalisasi: {knn_scaled_acc:.4f}")

from joblib import dump

# Menyimpan model GaussianNB
dump(gnb, 'gnb_model.joblib')
# Menyimpan model DecisionTree
dump(dt, 'dt_model.joblib')
# Menyimpan model KNN
dump(knn, 'knn_model.joblib')


import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# Judul aplikasi
st.title("Water Potability Prediction App")

# File uploader untuk mengunggah dataset CSV
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Membaca dataset
    df = pd.read_csv(uploaded_file)

    # Menampilkan dataset
    st.subheader("Dataset")
    st.write(df.head())

    # Menampilkan informasi umum tentang dataset
    st.subheader("Dataset Info")
    st.write(df.info())

    # Memeriksa missing values
    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    # Memisahkan fitur dan target
    X = df.drop(columns=["Potability"])
    y = df["Potability"]

    # Menangani missing values menggunakan imputasi rata-rata
    X = X.fillna(X.mean())

    # Normalisasi Data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Membagi data menjadi train dan test
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Resampling menggunakan SMOTE untuk menangani class imbalance
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    # Model Klasifikasi
    models = {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier()
    }

    # Menyimpan akurasi untuk setiap model
    model_accuracies = {}

    # Melatih dan menguji model
    for model_name, model in models.items():
        # Melatih model
        model.fit(X_train_resampled, y_train_resampled)

        # Prediksi
        y_pred = model.predict(X_test)

        # Menghitung akurasi
        accuracy = accuracy_score(y_test, y_pred)
        model_accuracies[model_name] = accuracy

        # Menampilkan confusion matrix
        st.subheader(f"Confusion Matrix - {model_name}")
        cm = confusion_matrix(y_test, y_pred)
        st.write(cm)

    # Menampilkan hasil perbandingan akurasi
    st.subheader("Model Accuracy Comparison")
    st.write(model_accuracies)

    # Visualisasi distribusi potability
    st.subheader("Potability Distribution")
    sns.countplot(x='Potability', data=df)
    plt.title('Distribution of Potability')
    st.pyplot()

    # Menampilkan histogram fitur numerik
    st.subheader("Histogram of Features")
    numerical_columns = X.columns
    for col in numerical_columns:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col], kde=True, bins=20)
        plt.title(f'Distribution of {col}')
        st.pyplot()

    # Fitur prediksi
    st.subheader("Make Prediction")
    st.write("Choose the features for prediction:")
    input_values = {}
    for col in numerical_columns:
        input_values[col] = st.slider(f"Select {col}", min_value=float(df[col].min()), max_value=float(df[col].max()), value=float(df[col].mean()))

    input_data = np.array(list(input_values.values())).reshape(1, -1)
    input_data_scaled = scaler.transform(input_data)

    # Prediksi menggunakan model terbaik (misalnya RandomForest)
    best_model = RandomForestClassifier(random_state=42)
    best_model.fit(X_train_resampled, y_train_resampled)
    prediction = best_model.predict(input_data_scaled)

    if prediction == 1:
        st.write("The water is Potable")
    else:
        st.write("The water is Not Potable")
