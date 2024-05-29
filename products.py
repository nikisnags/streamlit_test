import streamlit as st
import streamlit.components.v1 as stc

import pandas as pandas
import numpy as np
from pathlib import Path
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
import matplotlib
matplotlib.use('Agg') # TkAgg
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import base64 
import altair as alt
import plotly.express as px
timestr = time.strftime("%Y%m%d-%H%M%S")		
from solar_ml import *
from solar_dsm import *




import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
@st.cache
def load_data():
    df = pd.read_csv('Products.csv')
    df.Weight.fillna(df.Weight.mean(), inplace=True)
    df.OutletSize.fillna('Средний', inplace=True)
    return df

df = load_data()

# Заголовок
st.title('Анализ торгового предприятия')

# Просмотр данных
st.header('Таблица данных')
st.dataframe(df.head(15))

# Информация о данных
st.header('Информация о данных')
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

# Проверка на пропущенные значения
st.header('Пропущенные значения')
st.write(df.isnull().sum())

# Проверка на дубликаты
st.header('Дубликаты')
st.write(df.duplicated().sum())

# Анализ продаж по годам основания
st.header('Анализ продаж по годам основания')
st.write(df['EstablishmentYear'].value_counts())
st.write(df.groupby('EstablishmentYear')['OutletSales'].sum().astype(int))

# Анализ самого прибыльного магазина по году основания
st.header('Анализ самого прибыльного магазина по году основания')
sales_1985 = df[df['EstablishmentYear'] == 1985].groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False).head(12)
st.write(sales_1985)

# Гистограмма объема выручки
st.header('Гистограмма объема выручки')
fig, ax = plt.subplots()
ax.bar(x=sales_1985.index, height=sales_1985.values, color='grey')
ax.set_title('Объем выручки')
ax.set_ylabel('Сумма продаж')
ax.set_xlabel('Категории товаров')
plt.xticks(rotation=90)
for i, v in enumerate(sales_1985.values):
    ax.text(i, v, round(v), ha='center', va='bottom')
st.pyplot(fig)

# Круговая диаграмма объема выручки
st.header('Круговая диаграмма объема выручки')
fig, ax = plt.subplots()
ax.pie(sales_1985.values, labels=sales_1985.index, autopct='%.0f%%')
st.pyplot(fig)

# Анализ по категориям продуктов
st.header('Анализ по категориям продуктов')
st.write(df['ProductType'].value_counts())

# Новая таблица с категориями товаров
df_product = pd.DataFrame({
    'Категория товара': ['Фрукты и овощи', 'Закуски', 'Товары для дома', 'Замороженные продукты', 'Молочные продукты', 'Консервы', 'Выпечка', 'Здоровье и гигиена', 'Безалкогольные напитки', 'Мясо', 'Хлеб', 'Крепкие напитки', 'Другое', 'Бакалея', 'Завтрак', 'Морепродукты'],
    'Количество': [1232, 1200, 910, 856, 682, 649, 648, 520, 445, 425, 251, 214, 169, 148, 110, 64]
})
st.write(df_product)

# Гистограмма по категориям товаров
st.header('Гистограмма по категориям товаров')
fig, ax = plt.subplots()
df_product.groupby('Категория товара')['Количество'].mean().plot(ax=ax, kind='bar', rot=45, fontsize=10, figsize=(16, 10), color='purple')
st.pyplot(fig)

# Гистограмма самых продаваемых категорий товаров
st.header('Гистограмма самых продаваемых категорий товаров')
product_counts = df['ProductType'].value_counts()
fig, ax = plt.subplots()
ax.bar(x=product_counts.index, height=product_counts.values, color='red')
ax.set_title('Самые продаваемые категории товаров')
ax.set_xlabel('Категории товаров')
ax.set_ylabel('Количество продаж')
plt.xticks(rotation=90)
for i, v in enumerate(product_counts.values):
    ax.text(i, v, v, ha='center', va='bottom')
st.pyplot(fig)

# Гистограмма объема выручки по категориям товаров
st.header('Гистограмма объема выручки по категориям товаров')
product_sales = df.groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False)
fig, ax = plt.subplots()
ax.bar(x=product_sales.index, height=product_sales.values, color='green')
ax.set_title('Объем выручки')
ax.set_ylabel('Сумма продаж')
ax.set_xlabel('Категории товаров')
plt.xticks(rotation=90)
for i, v in enumerate(product_sales.values):
    ax.text(i, v, round(v), ha='center', va='bottom')
st.pyplot(fig)

# Анализ локаций магазинов
st.header('Анализ локаций магазинов')
st.write(df['LocationType'].value_counts())

df_location = pd.DataFrame({
    'Магазин': ['Локация 1', 'Локация 2', 'Локация 3'],
    'Количество продаж': [2388, 2785, 3350]
})
st.write(df_location)

# Круговая диаграмма по локациям
st.header('Круговая диаграмма по локациям')
location_sales = df.groupby('LocationType')['OutletSales'].sum()
fig, ax = plt.subplots()
ax.pie(location_sales.values, labels=location_sales.index, autopct='%.0f%%')
st.pyplot(fig)
