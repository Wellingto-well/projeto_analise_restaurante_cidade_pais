import pandas as pd
from folium.plugins import MarkerCluster
import folium
from streamlit_folium import folium_static
import streamlit as st

df = pd.read_csv('zomato.csv')

st.set_page_config(page_title="Home", page_icon="📊", layout="wide")

#TRATANDO DADOS

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
COLORS = {

"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

# transformando os id dos paises em nome
def country_name(country_id):
    return COUNTRIES[country_id]

# transformando os id das cores em nome
def color_name(color_code):
    return COLORS[color_code]   

#tratando dados
def clean_code(df):
    lista_com_codigo_de_cada_pais = df['Country Code']
    lista_correta_para_receber_nome_pais=[]
    for nomeando in lista_com_codigo_de_cada_pais:
        lista_correta_para_receber_nome_pais.append(country_name(nomeando))
    df['Country Name'] = lista_correta_para_receber_nome_pais


    recebendo_codigo_das_cores = df['Rating color']
    lista_com_o_nome_das_cores =[]
    for nome_cores in recebendo_codigo_das_cores:
        lista_com_o_nome_das_cores.append(color_name(nome_cores))
    df['Color Name'] = lista_com_o_nome_das_cores


    df_Cuisines_sem_na = df["Cuisines"].dropna()
    df_Cuisines_sem_na.isna().unique()
    df["Cuisines"] = df_Cuisines_sem_na.apply(lambda x: x.split(",")[0])
    
    return df

#criando mapa
def criação_do_mapa(df):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in df.iterrows():

        name = line["Restaurant Name"]
        price_for_two = line["Average Cost for two"]
        cuisine = line["Cuisines"]
        currency = line["Currency"]
        rating = line["Aggregate rating"]
        color = f'{line["Color Name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["Latitude"], line["Longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    return folium_static(m, width=1024, height=768)

#filtro para as infos do mapa
def filtro_para_mapa(df):
    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Escolha os Paises que Deseja visualizar os Restaurantes",
        df.loc[:, "Country Name"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    return list(countries)


df = clean_code(df)

st.markdown('# Fome Zero!')
st.header('O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.header('Temos as seguintes marcas dentro da nossa plataforma:')


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        id_restaurantes_unicos = df['Restaurant ID'].unique()

        st.metric('Restaurante cadastrado',len(id_restaurantes_unicos))

    with col2:
        id_paises_unicos = df['Country Code'].unique()
        st.metric('Países cadastrados',len(id_paises_unicos))
    
    with col3:
        cidade_unica = df['City'].unique()
        st.metric('Cidades cadastradas',len(cidade_unica))

    with col4:
        qntd_de_avaliacao = df['Aggregate rating'].count()
        st.metric('Quantidade de avaliações feitas', qntd_de_avaliacao)

    with col5:
        tipos_culinarios_unicos = df['Cuisines'].unique()
        st.metric('Total de culinarias oferecidas', len(tipos_culinarios_unicos))

with st.container():
    criação_do_mapa(df.loc[df["Country Name"].isin(filtro_para_mapa(df)), :])
