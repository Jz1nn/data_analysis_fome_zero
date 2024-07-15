# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# Bibliotecas necessárias
import inflection
import folium
import pandas as pd
import streamlit as st
import datetime as dt
from PIL import Image
from streamlit_folium import folium_static
pd.DataFrame.iteritems = pd.DataFrame.items

st.set_page_config(page_title='Visão Cidades', page_icon='📈', layout='wide')

# ----------------------------------------
# Funcoes
# ----------------------------------------
def top_cities_with_most_restaurants(df1):
    cols = ['city', 'restaurant_id', 'country_code']
    # selecao de linhas
    df_aux = df1.loc[:, cols].groupby(['city', 'country_code']).count().reset_index().sort_values(by='restaurant_id', ascending=False).head(10)

    # Desenhar o grafico de barras
    fig = px.bar(df_aux, x='city', y='restaurant_id', 
                 labels={'restaurant_id': 'Quantidade de Restaurantes', 'city': 'Cidade', 'country_code': 'País'}, 
                 title='Top 10 Cidades com mais Restaurantes',
                 color='country_code')
    
    return fig


def cities_with_restaurant_rating_up4(df1):
    filtro = df1['aggregate_rating'] > 4
    cols = ['city', 'restaurant_id', 'country_code']

    # selecao de linhas
    df_aux = df1.loc[filtro, cols].groupby(['city', 'country_code']).count().reset_index().sort_values(by='restaurant_id', ascending=False).reset_index().head(10)

    # Desenhar o grafico de barras
    fig = px.bar(df_aux, x='city', y='restaurant_id', 
                 labels={'restaurant_id': 'Quantidade de Restaurantes', 'city': 'Cidade', 'country_code': 'País'}, 
                 title='Cidades com Restaurantes com Média de Avaliação acima de 4',
                 color='country_code')

    return fig


def cities_with_restaurant_rating_down4(df1):
    filtro = df1['aggregate_rating'] < 4
    cols = ['city', 'restaurant_id', 'country_code']

    # selecao de linhas
    df_aux = df1.loc[filtro, cols].groupby(['city', 'country_code']).count().reset_index().sort_values(by='restaurant_id', ascending=False).reset_index().head(10)

    # Desenhar o grafico de barras
    fig = px.bar(df_aux, x='city', y='restaurant_id', 
                 labels={'restaurant_id': 'Quantidade de Restaurantes', 'city': 'Cidade', 'country_code': 'País'}, 
                 title='Cidades com Restaurantes com Média de Avaliação abaixo de 4',
                 color='country_code')

    return fig


def top_cities_most_cuisines(df1):
    cols = ['city', 'cuisines', 'country_code']
    # selecao de linhas
    df_aux = df1.loc[:, cols].groupby(['city', 'country_code']).nunique().reset_index().sort_values(by='cuisines', ascending=False).head(10)

    # Desenhar o grafico de barras
    fig = px.bar(df_aux, x='city', y='cuisines', 
                 labels={'cuisines': 'Quantidade de Culinárias Distintas', 'city': 'Cidade', 'country_code': 'País'}, 
                 title='Top 10 Cidades com mais Culinárias Distintas',
                 color='country_code')
    
    return fig


# -----------------------
# Import dataset
# -----------------------
df = pd.read_csv('dataset/zomato.csv')

# ----------------------------------------
# Renomear colunas do DataFrame
# ----------------------------------------
def rename_columns(df):
    df1 = df.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1

df1 = rename_columns(df)


# ----------------------------------------
# Preenchendo o nome dos paises
# ----------------------------------------
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]

df1['country_code'] = df1['country_code'].apply(country_name)


# -------------------------------------------------------------------
# Categorizar todos os restaurantes somente por um tipo de culinária
# -------------------------------------------------------------------
df1["cuisines"] = df1.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])


# --------------------------------------
# Criar tipo de categoria de comida
# --------------------------------------
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
df1['price_range'] = df1['price_range'].apply(create_price_tye)


# --------------------------------------
# Criar nome das cores
# --------------------------------------
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

df1['rating_color'] = df1['rating_color'].apply(color_name)


# --------------------------------------
# Remover duplicatas
# --------------------------------------
df1 = df1.drop_duplicates()


# --------------------------------------
# Apagando linhas com valores nulos das colunas (restaurant_id, restaurant_name, country_code, city, address, locality, locality_verbose, longitude,
# latitude, cuisines, average_cost_for_two, currency, price_range, aggregate_rating, rating_color, rating_text, votes)
# --------------------------------------
df1 = (df1.dropna(subset=['restaurant_id', 'restaurant_name', 'country_code', 'city', 'address', 'locality', 'locality_verbose', 
                          'longitude', 'latitude', 'cuisines', 'average_cost_for_two', 'currency', 'price_range', 'aggregate_rating', 
                          'rating_color', 'rating_text', 'votes']))

# -------------------------- Inicio da estrutura logica do codigo --------------------------

# ===============================
# Barra Lateral
# ===============================
st.header('🏙️ Visão Cidades')

image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=60)

st.sidebar.markdown('## Filtros')

country_options = st.sidebar.multiselect(
    'Escolha os paises que deseja visualizar as informações',
    ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 
     'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 
     'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'],
    default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by John Willian.')

# Filtro de pais
linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]

# ===============================
# Layout no Streamlit
# ===============================

with st.container():
    # Top 10 cidades mais restaurantes
    fig = top_cities_with_most_restaurants(df1)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Cidades com restaurantes com media de av. acima
        fig = cities_with_restaurant_rating_up4(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Cidades com restaurantes com media de av. abaixo
        fig = cities_with_restaurant_rating_down4(df1)
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    # Top 10 cidades culinarias distintas
    fig = top_cities_most_cuisines(df1)
    st.plotly_chart(fig, use_container_width=True)
