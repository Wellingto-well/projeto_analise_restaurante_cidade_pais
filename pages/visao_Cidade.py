import streamlit as st
import pandas as pd
import plotly.express as px 

df = pd.read_csv('pages\\zomato.csv')

st.set_page_config(page_title="Cities", page_icon="🏙️", layout="wide")
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

# tratando dados
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

df = clean_code(df)

# funç~~ao do filtro
def filtro(df):
    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Escolha os Paises que Deseja visualizar as Informações",
        df.loc[:, "Country Name"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    return list(countries)

# filtro
countries = filtro(df)

# top restaurante baseado no filtro
def top10_restaurante(df,countries):
    grouped_df_top10_restaurantes = (
            df.loc[df["Country Name"].isin(countries), ["Restaurant ID", "Country Name", "City"]]
            .groupby(["Country Name", "City"])
            .count()
            .sort_values(["Restaurant ID", "City"], ascending=[False, True])
            .reset_index()
        )

    fig = px.bar(grouped_df_top10_restaurantes, x='City', y='Restaurant ID', text_auto=True, height=400, title='top 10 cidades com mais restaurente  na base de dados')
    return st.plotly_chart(fig,use_container_width=True)

# quantidade de resutaurante com boas notas por cidade
def top7_cidades_restaurantes_acima4(df,countries):
    grouped_df = (
    df.loc[
        (df["Aggregate rating"] >= 4) & (df["Country Name"].isin(countries)),
        ["Restaurant ID", "Country Name", "City"],
    ]
    .groupby(["Country Name", "City"])
    .count()
    .sort_values(["Restaurant ID", "City"], ascending=[False, True])
    .reset_index()
)
    fig = px.bar(grouped_df, x='City', y='Restaurant ID', text_auto=True, title='as 7 cidades com restaurentes com avaliação maior que 4')
    return st.plotly_chart(fig, use_container_width=True)

# quantidade de resutaurante com notas ruins por cidade
def top7_cidades_restaurantes_abaixo2_5(df,countries):
    grouped_df = (
    df.loc[
        (df["Aggregate rating"] <= 2.5) & (df["Country Name"].isin(countries)),
        ["Restaurant ID", "Country Name", "City"],
    ]
    .groupby(["Country Name", "City"])
    .count()
    .sort_values(["Restaurant ID", "City"], ascending=[False, True])
    .reset_index()
)
    fig = px.bar(grouped_df, x='City', y='Restaurant ID', text_auto=True,  title='top7 cidade com restaurentes com media de avaiação abaixo de 2,5')
    return st.plotly_chart(fig, use_container_width=True)

st.header("Visão Cidades")


with st.container():
    top10_restaurante(df,countries)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        top7_cidades_restaurantes_acima4(df,countries)
    
    with col2:
        top7_cidades_restaurantes_abaixo2_5(df,countries)


