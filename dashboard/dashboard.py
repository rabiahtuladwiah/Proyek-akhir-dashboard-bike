import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

bike_df=pd.read_csv("https://raw.githubusercontent.com/rabiahtuladwiah/Proyek-akhir-dashboard-bike/main/dashboard/bike.csv")

#mengubah weather_labels
weather_labels = {
    1: 'cerah',
    2: 'berawan',
    3: 'hujan ringan',
    4: 'hujan lebat'
}

#mengubah season_labels
season_labels = {
    1: 'springer',
    2: 'summer',
    3: 'fall',
    4: 'winter'
}
# Membuat kolom baru dengan label cuaca
bike_df['season_label_day'] = bike_df['season_day'].map(season_labels)

# Membuat kolom baru dengan label cuaca
bike_df['weather_label_day'] = bike_df['weathersit_day'].map(weather_labels)

# Fungsi untuk analisis harian
def create_daily_analysis_df(df):
    daily_analysis_df = df.groupby(by='weekday_day').agg({
        'cnt_day': 'sum'
    }).reset_index()
    return daily_analysis_df

# Fungsi untuk analisis per jam
def create_hourly_analysis_df(df):
    hourly_analysis_df = df.groupby(by='hr').agg({
        'cnt_hour':'sum'
    }).reset_index()
    return hourly_analysis_df

# Fungsi untuk analisis hari libur
def create_holiday_analysis_df(df):
    holiday_analysis_df = df.groupby(by='holiday_day')[['cnt_day']].mean().reset_index()
    return holiday_analysis_df

# Fungsi untuk analisis cuaca harian
def create_daily_weather_analysis_df(df):
    daily_weather_analysis_df = df.groupby(by='weather_label_day')['cnt_day'].mean().reset_index()
    return daily_weather_analysis_df

# Fungsi untuk analisis cuaca harian
def create_season_analysis_df(df):
    daily_season_analysis_df = df.groupby(by='season_label_day')['cnt_day'].mean().reset_index()
    return daily_season_analysis_df

# Fungsi untuk analisis tahunan
def yearly_analysis_df(df):
    yearly_analysis_df = df.groupby(by='yr_day')['cnt_day'].mean().reset_index()
    return yearly_analysis_df

with st.sidebar:
    # URL raw gambar dari GitHub
    image_url = "https://raw.githubusercontent.com/rabiahtuladwiah/Proyek-akhir-dashboard-bike/main/dashboard/bike.jpg"
    st.image(image_url, use_column_width=True)
    
    visualization_options = ['Analisis Harian', 'Analisis Per Jam', 'Analisis pada Hari Libur', 'Analisis Cuaca Harian', 'Analisis Musim', 'Analisis Tahunan']
    visualization_choice = st.selectbox('Pilih Visualisasi Pengguna Sepeda', visualization_options)


st.title('Dashboard Analisis Penggunaan Sepeda')

# Main Content
if visualization_choice == 'Analisis Harian':
    st.subheader('Analisis Penggunaan Sepeda Harian')
    daily_analysis_data = create_daily_analysis_df(bike_df)
    def plot_daily_analysis(data):
        plt.figure(figsize=(10, 6))
        sns.barplot(x='weekday_day', y='cnt_day', data=data, palette='viridis')
        plt.xlabel('Hari dalam Seminggu')
        plt.ylabel('Jumlah Sepeda (Rata-rata)')
    plot_daily_analysis(daily_analysis_data)
    st.pyplot(plt.gcf())

elif visualization_choice == 'Analisis Per Jam':
    st.subheader('Analisis Penggunaan Sepeda Per Jam')
    hourly_analysis_data = create_hourly_analysis_df(bike_df)
    def plot_hourly_analysis(data):
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='hr', y='cnt_hour', data=data)
        plt.xlabel('Jam dalam Sehari')
        plt.ylabel('Jumlah Sepeda (Rata-rata)')
        plt.xticks(range(24), labels=[str(i) for i in range(24)])
    plot_hourly_analysis(hourly_analysis_data)
    st.pyplot(plt.gcf())

elif visualization_choice == 'Analisis pada Hari Libur':
    st.subheader('Analisis Penggunaan Sepeda pada Hari Libur')
    holiday_analysis_data = create_holiday_analysis_df(bike_df)
    def plot_holiday_analysis(data):
        plt.figure(figsize=(8, 6))
        sns.barplot(x='holiday_day', y='cnt_day', data=data, palette='dark')
        plt.xlabel('Status Hari')
        plt.ylabel('Jumlah Sepeda (Rata-rata)')
        plt.xticks([0, 1], ['Bekerja', 'Libur'])
    plot_holiday_analysis(holiday_analysis_data)
    st.pyplot(plt.gcf())

elif visualization_choice == 'Analisis Cuaca Harian':
    st.subheader('Analisis Penggunaan Sepeda Berdasarkan Cuaca Harian')
    daily_weather_analysis_data = create_daily_weather_analysis_df(bike_df)
    def plot_daily_weather_analysis(data):
        plt.figure(figsize=(10, 6))
        sns.barplot(x='weather_label_day', y='cnt_day', data=data, palette='muted')
        plt.xlabel('Faktor Cuaca')
        plt.ylabel('Jumlah Sepeda (Rata-rata)')
    plot_daily_weather_analysis(daily_weather_analysis_data)
    st.pyplot(plt.gcf())

elif visualization_choice == 'Analisis Musim':
    st.subheader('Analisis Penggunaan Sepeda Berdasarkan Musim')
    daily_season_analysis_data = create_season_analysis_df(bike_df)
    def plot_daily_season_analysis(data):
        plt.figure(figsize=(10, 6))
        sns.barplot(x='season_label_day', y='cnt_day', data=data, palette='viridis')
        plt.xlabel('Musim')
        plt.ylabel('Jumlah Sepeda (Rata-rata)')
    plot_daily_season_analysis(daily_season_analysis_data)
    st.pyplot(plt.gcf())

elif visualization_choice == 'Analisis Tahunan':
    st.subheader('Analisis Penggunaan Sepeda Tahunan')
    yearly_analysis_data = yearly_analysis_df(bike_df)
    def plot_yearly_analysis(data):
        plt.figure(figsize=(8, 6))
        sns.barplot(x='yr_day', y='cnt_day', data=data, palette='pastel')
        plt.xlabel('Tahun')
        plt.ylabel('Jumlah Sepeda (Rata-rata)')
        plt.xticks([0, 1], ['2011', '2012'])
    plot_yearly_analysis(yearly_analysis_data)
    st.pyplot(plt.gcf())
