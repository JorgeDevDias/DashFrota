import pandas as pd
import requests
import streamlit as st
import json

st.set_page_config(page_title='Dash Frota',layout='wide')
with st.container():
    st.title('Dashbord Frota')
    st.write('---')


@st.cache_data
def carregar_dados():
    dados_api_tt = requests.get('https://frotafroteq.bubbleapps.io/api/1.1/obj/acompanhamentoFrota')
    dados_dic_tt = dados_api_tt.json()
    df_tt = pd.DataFrame(dados_dic_tt['response']['results'])
    df_tt = df_tt[['Motorista','Prefixo','Status','Tipo de Equipamento','Cidade Atual','Atendimento','Chegada (Origem)','Chegada (Destino)','Saída (Origem)','Observação_VIX']]
    return df_tt

df_tt = carregar_dados()
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_tt)

st.download_button(
    label="Download dados em CSV",
    data=csv,
    file_name='status.csv',
    mime='text/csv',
)


df_tt = carregar_dados()

status_tt = df_tt[['Status', 'Prefixo']]
status_tt = status_tt.groupby('Status').count()
status_tt = status_tt.sort_values('Prefixo', ascending=False)
op_status_tt = df_tt.Status.unique().tolist()
op_cidade_tt = df_tt['Cidade Atual'].unique().tolist()
op_tipo_tt = df_tt['Tipo de Equipamento'].unique().tolist()

with st.container():
    st.subheader('Frota TT')
    cidade = st.selectbox('Cidade Atual', op_cidade_tt)
    status = st.selectbox('Status da Frota',op_status_tt)
    #tipo = st.selectbox('Status da Frota', op_tipo_tt)
    df_tt_filtrado = df_tt[(df_tt['Status'] == status) & (df_tt['Cidade Atual'] == cidade)]
    st.dataframe(df_tt_filtrado)