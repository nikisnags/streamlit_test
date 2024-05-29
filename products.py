import streamlit as st
import pandas as pd
import io
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
"""Просматриваем нашу таблицу с  помощью **head()**"""
st.header('Таблица данных')
st.dataframe(df.head(15))

# Информация о данных
"""**Для удобства пометим название столбцов и их типовое назначение в датасете**
*   **ProductID** : уникальный идентификатор товара
*   **Weight** : вес продуктов
*  **FatContent** : указывает, содержит ли продукт мало жира или нет
*   **Visibility** : процент от общей площади витрины всех товаров в магазине, отведенный для конкретного продукта
*   **ProductType** : категория, к которой относится товар
*   **MRP** : Максимальная розничная цена (указанная цена) на продукты
*   **OutletID**: уникальный идентификатор магазина
*   **EstablishmentYear** : год основания торговых точек
*   **OutletSize** : размер магазина с точки зрения занимаемой площади
*   **LocationType** : тип города, в котором расположен магазин
*   **OutletType** : указывает, является ли торговая точка просто продуктовым магазином или каким-то супермаркетом
*   **OutletSales** : (целевая переменная) продажи товара в конкретном магазине

Чтобы узнать более подробную информацию о количестве строк, столбцов и тип данных используем **info()**
"""
st.header('Информация о данных')
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

# Проверка на пропущенные значения
"""Проанализируем количество нулевых значений в стобцах с помощью функции **"data.isnull().sum()"**"""
st.header('Пропущенные значения')
st.write(df.isnull().sum())

"""В результате анализа мы видим, что в столбцах **"Weight"** - 1463 и **"OutletSize"** - 2410 нулевых значения соответсвенно.

Заполняем нулевые значения с помощью **fillna()**. Ячейки заполнятся средними значениями по всему столбцу с учетом анализа всех данных.
"""



# Проверка на дубликаты
"""Теперь удалим дубликаты, если такие имеются с помощью **duplicated()**"""
st.header('Дубликаты')
st.write(df.duplicated().sum())

# Анализ продаж по годам основания
"""# Анализ продаж по годам основания

Смотрим количество продаж магазина по году основания, влияет ли это как-то на статистику с помощью **value_counts()**
"""
st.header('Анализ продаж по годам основания')
st.write(df['EstablishmentYear'].value_counts())
"""На основе данной таблицы, можно сделать вывод, что магазин, основанный в 1985 году имеет самое большое количество продаж и в 1998 самое маленькое соотвественно.
С помощью **groupby()** узнаем количесвто выручки.
"""
st.write(df.groupby('EstablishmentYear')['OutletSales'].sum().astype(int))

# Анализ самого прибыльного магазина по году основания
"""# Анализ самого прибыльного магазина по году основания
С помощью **groupby()** выведем таблицу с категорями товаров в количестве 6, чтобы понять, что принесло самую большую прибыль магазину, который основан в 1985 году.
"""
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
