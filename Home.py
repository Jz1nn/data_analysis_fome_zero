import streamlit as st
import pandas as pd
import folium

from PIL import Image
from streamlit_folium import folium_static

# --------------------------------------
# Configuracao da pagina
# --------------------------------------
st.set_page_config(
    page_title='Main Page',
    page_icon='🎲'
)

# --------------------------------------
# Limpeza de dados
# --------------------------------------

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

# ------------------------------------- PAGINA -------------------------------------
# ===============================
# Barra Lateral
# ===============================
image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=60)
st.sidebar.markdown('## Fome Zero!')


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


st.write('# Fome Zero!')

st.markdown(
    """
    ## O Melhor lugar para encontrar seu mais novo restaurante favorito!

    ### Temos as seguintes marcas dentro da nossa plataforma:
    """)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    restaurant_unique = len(df1.loc[:, 'restaurant_id'].unique())
    col1.metric('Restaurantes Cadastrados', restaurant_unique)

with col2:
    country_unique = len(df1.loc[:, 'country_code'].unique())
    col2.metric('Paises Cadastrados', country_unique)

with col3:
    city_unique = len(df1.loc[:, 'city'].unique())
    col3.metric('Cidades Cadastradas', city_unique)

with col4:
    avaliation_unique = df1.loc[:, 'votes'].sum()
    col4.metric('Avaliações Feitas', avaliation_unique)

with col5:
    cuisines_unique = len(df1.loc[:, 'cuisines'].unique())
    col5.metric('Tipos de Culinárias', cuisines_unique)

# Agrupar e calcular a média dos custos e classificações por cidade
df_aux = df1.groupby('city').agg({
    'average_cost_for_two': 'mean',
    'cuisines': 'first',  # Lista de tipos de culinárias na cidade
    'aggregate_rating': 'mean',
    'latitude': 'mean',
    'longitude': 'mean'
}).reset_index()

# Criar o mapa
map = folium.Map(zoom_start=2)

# Adicionar os marcadores ao mapa
for index, location_info in df_aux.iterrows():
    folium.Marker(
        location=[location_info['latitude'], location_info['longitude']],
        popup=(
            f"<b>Cidade:</b> {location_info['city']}<br>"
            f"<b>Culinárias:</b> {location_info['cuisines']}<br>"
            f"<b>Custo Médio para Dois:</b> {location_info['average_cost_for_two']:.2f}<br>"
            f"<b>Avaliação Média:</b> {location_info['aggregate_rating']:.1f}"
        )
    ).add_to(map)

# Exibir o mapa no Streamlit
folium_static(map, width=1024, height=600)

#  ### Precisa de ajuda?
# - John (xx)xxxxx-xxxx
