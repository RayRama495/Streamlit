import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Menambahkan judul aplikasi
st.title("Aplikasi Streamlit Pertama Saya")

# Menampilkan teks
st.write("Selamat datang di aplikasi pertama Anda dengan Streamlit!")

# Membuat data untuk grafik
data = np.random.randn(100)

# Menampilkan histogram
fig, ax = plt.subplots()
ax.hist(data, bins=10)
st.pyplot(fig)

# Menambahkan input dari pengguna
name = st.text_input("Masukkan nama Anda:")
st.write(f"Hallo, {name}!")
