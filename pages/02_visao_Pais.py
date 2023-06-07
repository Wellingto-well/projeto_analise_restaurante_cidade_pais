import streamlit as st
import pandas as pd
import plotly.express as px 

df = pd.read_csv('pages\\zomato.csv')

st.set_page_config(page_title="Países", page_icon="🌍", layout="wide")

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

# filtro
def filtro(df):
    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Escolha os Paises que Deseja visualizar as Informações",
        df.loc[:, "Country Name"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    return list(countries)

taxas_cambio = {
    'Botswana Pula(P)': 13.62,
    'Brazilian Real(R$)': 4.91,
    'Dollar($)': 1.0,
    'Emirati Diram(AED)': 3.67,
    'Indian Rupees(Rs.)': 82.52,
    'Indonesian Rupiah(IDR)': 0.000067,
    'NewZealand($)': 0.61,
    'Pounds(£)': 1.24,
    'Qatari Rial(QR)': 0.27,
    'Rand(R)': 0.052,
    'Sri Lankan Rupee(LKR)': 0.0034,
    'Turkish Lira(TL)': 0.046
}

# Função para converter o valor para dólar
def converter_para_dolar(moeda, valor):
    taxa = taxas_cambio[moeda]
    return valor * taxa

# Criando a nova coluna 'Valor em Dólar'
df['Valor em Dolar'] = df.apply(lambda row: converter_para_dolar(row['Currency'], row['Average Cost for two']), axis=1)

countries = filtro(df)
# quantidade de restaurante por pais 
def quantidade_de_restaurante(df, countries):
    grouped_df = (
    df.loc[df["Country Name"].isin(countries), ["Restaurant ID", "Country Name"]]
    .groupby("Country Name")
    .count()
    .sort_values("Restaurant ID", ascending=False)
    .reset_index()
    )
    fig = px.bar(grouped_df, x='Country Name', y='Restaurant ID', text_auto=True, height=430, title='Quantidade de restaurantes registrado por país')
    return st.plotly_chart(fig, use_container_width=True)

# quantidade de cidades por pais
def quantidade_de_cidades_por_pais(df,countries):
    grouped_df = (
    df.loc[df["Country Name"].isin(countries), ["City", "Country Name"]]
    .groupby("Country Name")
    .nunique()
    .sort_values("City", ascending=False)
    .reset_index()
)
    fig = px.bar(grouped_df, x='Country Name', y='City', text_auto=True, height=400, title='Quantidade de cidades resgistrada por país')
    return st.plotly_chart(fig, use_container_width=True)

# media de avaliação por pais
def media_avaliacao_feita_pais(df, countries):
    grouped_df = (
    df.loc[df["Country Name"].isin(countries), ["Votes", "Country Name"]]
    .groupby("Country Name")
    .mean()
    .sort_values("Votes", ascending=False)
    .reset_index()
)
    fig = px.bar(grouped_df, x='Country Name', y='Votes', text_auto=True, height=400, title='media de avaliações feitas por pais')
    return st.plotly_chart(fig, use_container_width=True)

# media de preço no prato para 2 pessoas
def media_de_preço_prato_2_pessoas(df, countries):
    grouped_df = (
    df.loc[df["Country Name"].isin(countries), ["Valor em Dolar", "Country Name"]]
    .groupby("Country Name")
    .mean()
    .sort_values("Valor em Dolar", ascending=False)
    .reset_index()
)
    fig = px.bar(grouped_df, x='Country Name', y='Valor em Dolar', text_auto=True, height=400, title='media de preço de um prato para duas pessoas por país')
    st.plotly_chart(fig, use_container_width=True)



st.title('Visão País')

with st.container():
    quantidade_de_restaurante(df, countries)

with st.container():
    quantidade_de_cidades_por_pais(df,countries)

with st.container():

    col1, col2 = st.columns(2)

    with col1:
        media_avaliacao_feita_pais(df, countries)

    with col2:
        media_de_preço_prato_2_pessoas(df, countries)


