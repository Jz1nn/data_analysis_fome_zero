# Libraries
#from haversine import haversine
import plotly.express as px
#import plotly.graph_objects as go

# Bibliotecas necessárias
import inflection
#import folium
import pandas as pd
import streamlit as st
#import datetime as dt
from PIL import Image
#from streamlit_folium import folium_static
pd.DataFrame.iteritems = pd.DataFrame.items

st.set_page_config(page_title='Visão Paises', page_icon='📈', layout='wide')

# ----------------------------------------
# Funcoes
# ----------------------------------------
def restaurant_by_country(df1):
    cols = ['restaurant_id', 'country_code']
    # selecao de linhas
    df_aux = (df1.loc[:, cols]
              .groupby('country_code')
              .count()
              .reset_index()
              .sort_values(by='restaurant_id', ascending=False))
    
    # Desenhar o grafico de barras
    fig = px.bar(df_aux, x='country_code', y='restaurant_id', 
                 labels={'restaurant_id': 'Quantidade de Restaurantes', 'country_code': 'País'}, 
                 title='Quantidade de Restaurantes por País')

    return fig


def cities_by_country(df1):
    cols = ['city', 'country_code']
    # selecao de linhas
    df_aux = df1.loc[:, cols].groupby('country_code').nunique().reset_index().sort_values(by='city', ascending=False)

    # Desenhar o grafico de barras
    fig = px.bar(df_aux, x='country_code', y='city', 
                 labels={'city': 'Quantidade de Cidades', 'country_code': 'País'}, 
                 title='Quantidade de Cidades por País')
    
    return fig


def mean_rating_by_country(df1):
    cols = ['votes', 'country_code']
    # selecao de linhas
    df_aux = df1.loc[:, cols].groupby('country_code').mean().reset_index().sort_values(by='votes', ascending=False)

    # Desenhar o grafico de barras
    fig = px.bar(df_aux, x='country_code', y='votes', 
                 labels={'votes': 'Média de Avaliações', 'country_code': 'País'}, 
                 title='Média de Avaliações por País')
    
    return fig


def mean_cost_for_two_by_country(df1):
    cols = ['average_cost_for_two', 'country_code']
    # selecao de linhas
    df_aux = df1.loc[:, cols].groupby('country_code').mean().reset_index().sort_values(by='average_cost_for_two', ascending=False)

    # Desenhar o grafico de barras
    fig = px.bar(df_aux, x='country_code', y='average_cost_for_two', 
                 labels={'average_cost_for_two': 'Média de Custo para Dois', 'country_code': 'País'}, 
                 title='Média de Custo para Dois por País')
    
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
st.header('🌎 Visão Países')

image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=60)

st.sidebar.markdown('## Filtros')

country_options = st.sidebar.multiselect(
    'Escolha os paises que deseja visualizar as informações',
    df1['country_code'].unique(),
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
    # Restaurantes por Pais
    fig = restaurant_by_country(df1)
    st.plotly_chart(fig, use_container_witdth=True)

with st.container():
    # Cidades por Pais
    fig = cities_by_country(df1)
    st.plotly_chart(fig, use_container_witdth=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        # Media de avaliacoes por pais
        fig = mean_rating_by_country(df1)
        st.plotly_chart(fig, use_container_witdth=True)

    with col2:
        # Media de preco prato para 2 pessoas por pais
        fig = mean_cost_for_two_by_country(df1)
        st.plotly_chart(fig, use_container_witdth=True)
