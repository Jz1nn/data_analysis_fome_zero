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

st.set_page_config(page_title='Visão Cozinhas', page_icon='🍽️', layout='wide')

# ----------------------------------------
# Funcoes
# ----------------------------------------
def top_cuisines_types(df1, top_asc, top):
    cols = ['cuisines', 'aggregate_rating']
    # selecao de linhas
    df_aux = df1.loc[:, cols].groupby('cuisines').mean().reset_index().sort_values(by='aggregate_rating', ascending=top_asc).head(10)
    
    # Desenhar o grafico de barras
    fig = px.bar(df_aux, x='cuisines', y='aggregate_rating', 
                 labels={'aggregate_rating': 'Media de Avaliação Média', 'cuisines': 'Tipo de Culinária'}, 
                 title=f'Top {top} Tipos de Culinária (baseado no filtro)',
                 color='cuisines')
    
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
st.header('🍽️ Visão Tipos de Cozinhas')

st.sidebar.markdown('## Filtros')

country_options = st.sidebar.multiselect(
    'Escolha os paises que deseja visualizar as informações',
    df1['country_code'].unique(),
    default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

number_restaurants = st.sidebar.slider(
    'Selecione a quantidade de Restaurantes que deseja visualizar',
    min_value=1,
    max_value=20,
    value=10)

cuisines_types = st.sidebar.multiselect(
    'Escolha os tipos de culinária que deseja visualizar',
    df1['cuisines'].unique(),
    default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by John Willian.')

# Filtro de pais
linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de culinária
linhas_selecionadas = df1['cuisines'].isin(cuisines_types)
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de quantidade de restaurantes
df1 = df1.head(number_restaurants)

# ===============================
# Layout no Streamlit
# ===============================

st.markdown('### Melhores Restaurantes dos Principais tipos Culinários (baseado no filtro)')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5, gap='large')

    top_cuisines = df1.loc[:, ['cuisines', 'aggregate_rating']].sort_values(by='aggregate_rating', ascending=False)

    with col1:
        # Registrar apenas a nota da avaliação
        top_cuisine1 = top_cuisines['aggregate_rating'].values[0]

        # Registrar o nome da culinária
        cuisine_name1 = top_cuisines['cuisines'].values[0]
        col1.metric(cuisine_name1, f"{top_cuisine1}/5")

    with col2:
        top_cuisine2 = top_cuisines['aggregate_rating'].values[1]

        cuisine_name2 = top_cuisines['cuisines'].values[1]
        col2.metric(cuisine_name2, f"{top_cuisine2}/5")

    with col3:
        top_cuisine3 = top_cuisines['aggregate_rating'].values[2]

        cuisine_name3 = top_cuisines['cuisines'].values[2]
        col3.metric(cuisine_name3, f"{top_cuisine3}/5")

    with col4:
        top_cuisine4 = top_cuisines['aggregate_rating'].values[3]

        cuisine_name4 = top_cuisines['cuisines'].values[3]
        col4.metric(cuisine_name4, f"{top_cuisine4}/5")

    with col5:
        top_cuisine5 = top_cuisines['aggregate_rating'].values[4]

        cuisine_name5 = top_cuisines['cuisines'].values[4]
        col5.metric(cuisine_name5, f"{top_cuisine5}/5")

with st.container():
    # Dataframe com os 10 melhores restaurantes. cols = restaurant_id, restaurant_name, country_code, city, cuisines, average_cost_for_two, aggregate_rating, votes
    st.markdown('### Top 10 Restaurantes')

    # Selecionar as colunas e obter os top 10 por aggregate_rating
    df_aux = (df1.loc[:, ['restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating']]
                .groupby('aggregate_rating')
                .head(10)
                .reset_index(drop=True))

    # Renomear as colunas para o português
    df_aux = df_aux.rename(columns={
        'restaurant_name': 'Nome do Restaurante',
        'country_code': 'País',
        'city': 'Cidade',
        'cuisines': 'Culinária',
        'average_cost_for_two': 'Custo Médio para Dois',
        'aggregate_rating': 'Avaliação Media'
    })

    st.write(df_aux)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        # 10 melhores tipos de culinarias
        fig = top_cuisines_types(df1, top_asc=False, top='melhores')
        st.plotly_chart(fig)

    with col2:
        # 10 piores tipos de culinarias
        fig = top_cuisines_types(df1, top_asc=True, top='piores')
        st.plotly_chart(fig)