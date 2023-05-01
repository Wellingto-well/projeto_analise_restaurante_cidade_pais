import streamlit as st
import pandas as pd
import plotly.express as px 



df = pd.read_csv('pages\\zomato.csv')

st.set_page_config(page_title='Cuisines', page_icon='🍽️', layout='wide')

#TRATANDO DADOS

COUNTRIES = {
1: 'India',
14: 'Australia',
30: 'Brazil',
37: 'Canada',
94: 'Indonesia',
148: 'New Zeland',
162: 'Philippines',
166: 'Qatar',
184: 'Singapure',
189: 'South Africa',
191: 'Sri Lanka',
208: 'Turkey',
214: 'United Arab Emirates',
215: 'England',
216: 'United States of America',
}
COLORS = {

'3F7E00': 'darkgree',
'5BA829': 'gree',
'9ACD32': 'lightgree',
'CDD614': 'orang',
'FFBA00': 're',
'CBCBC8': 'darkre',
'FF7800': 'darkre',
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

    df_Cuisines_sem_na = df['Cuisines'].dropna()
    df_Cuisines_sem_na.isna().unique()
    df['Cuisines'] = df_Cuisines_sem_na.apply(lambda x: x.split(',')[0])
    
    return df

df = clean_code(df)

# criando filtro
def filto(df):
    st.sidebar.markdown('## Filtros')

    countries = st.sidebar.multiselect(
        'Escolha os Paises que Deseja visualizar as Informações',
        df.loc[:, 'Country Name'].unique().tolist(),
        default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'],
    )

    top_n = st.sidebar.slider(
        'Selecione a quantidade de Restaurantes que deseja visualizar', 1, 20, 10
    )

    cuisines = st.sidebar.multiselect(
        'Escolha os Tipos de Culinária ',
        df.loc[:, 'Cuisines'].unique().tolist(),
        default=[
            'Home-made',
            'BBQ',
            'Japanese',
            'Brazilian',
            'Arabian',
            'American',
            'Italian',
        ],
    )

    return list(countries), top_n, list(cuisines)


countries, top_n, cuisines = filto(df)

# fazendo top x restaurantes q o usuario pedir por culinaria e por pais
def top_restaurants(countries, cuisines, top_n, df):
    cols = [
        'Restaurant ID',
        'Restaurant Name',
        'Country Name',
        'City',
        'Cuisines',
        'Average Cost for two',
        'Aggregate rating',
        'Votes',
    ]

    lines = (df['Cuisines'].isin(cuisines)) & (df['Country Name'].isin(countries))

    dataframe = df.loc[lines, cols].sort_values(
        ['Aggregate rating', 'Restaurant ID'], ascending=[False, True]
    )

    return dataframe.head(top_n)

# top x culinaria
def top10_culinaria(df, top_n, countries):
    lines = df['Country Name'].isin(countries)

    grouped_df = (
        df.loc[lines, ['Aggregate rating', 'Cuisines']]
        .groupby('Cuisines')
        .mean()
        .sort_values('Aggregate rating', ascending=False)
        .reset_index()
        .head(top_n)
    )
    fig = px.bar(grouped_df, x='Cuisines', y='Aggregate rating', text_auto=True, height=400,title=f"Top {top_n} Melhores Tipos de Culinárias")
    return st.plotly_chart(fig, use_container_width=True)

# top x piores culinarias
def top10_piores_culinaria(df, top_n, countries):
    lines = df['Country Name'].isin(countries)

    grouped_df = (
        df.loc[lines, ['Aggregate rating', 'Cuisines']]
        .groupby('Cuisines')
        .mean()
        .sort_values('Aggregate rating', ascending=False)
        .reset_index()
        .head(top_n)
    )
    fig = px.bar(grouped_df, x='Cuisines', y='Aggregate rating', text_auto=True, height=400,title=f'Top {top_n} Piores Tipos de Culinárias')
    return st.plotly_chart(fig, use_container_width=True)

st.markdown('#  🍽️ Visão Tipos de Cusinhas')
st.header('Melhores Restaurantes dos Principais tipos Culinários')


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        maior_nota_north_indian = df[(df['Cuisines'] == 'North Indian') & (df['Aggregate rating'] >= 4.9)][['Aggregate rating']]
        maior_nota_north_indian =maior_nota_north_indian['Aggregate rating'].unique()
        st.metric('Culinaria: indiana', maior_nota_north_indian)
    
    with col2:
        maior_nota_American = df[(df['Cuisines'] == 'American') & (df['Aggregate rating'] >= 4.9)][['Aggregate rating']]
        maior_nota_American=maior_nota_American['Aggregate rating'].unique()
        st.metric('Culinaria: America',maior_nota_American)
    with col3:
        maior_nota_Pizza = df[(df['Cuisines'] == 'Pizza') & (df['Aggregate rating'] >= 4.9)][['Aggregate rating']]
        maior_nota_Pizza=maior_nota_Pizza['Aggregate rating'].unique()
        st.metric('Culinaria: Pizza',maior_nota_Pizza)
    with col4:
        maior_nota_Italian = df[(df['Cuisines'] == 'Italian') & (df['Aggregate rating'] >= 4.9)][['Aggregate rating']]
        maior_nota_Italian=maior_nota_Italian['Aggregate rating'].unique()
        st.metric('Culinaria: Italiana',maior_nota_Italian)    
    with col5:
        maior_nota_Chinese = df[(df['Cuisines'] == 'Chinese') & (df['Aggregate rating'] >= 4.9)][['Aggregate rating']]
        maior_nota_Chinese=maior_nota_Chinese['Aggregate rating'].unique()
        st.metric('Culinaria: Chinesa',maior_nota_Chinese)

with st.container():
    dataframe= top_restaurants(countries, cuisines, top_n, df)
    st.dataframe(dataframe)
    # top_10_restaurantes = df[df['Aggregate rating'] >= 4.9][['Restaurant ID','Restaurant Name','Country Name','City','Cuisines','Average Cost for two','Aggregate rating','Votes']].reset_index()
    # st.dataframe(top_10_restaurantes.head(10))

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        top10_culinaria(df, top_n, countries)
    
    with col2:
        top10_piores_culinaria(df, top_n, countries)