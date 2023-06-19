import pandas as pd
import requests
import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title='Dash Frota',layout='wide')
with st.container():
    st.title('Status Frota')
    st.write('---')


@st.cache_data
def carregar_dados_tt():
    dados_api_tt = requests.get('https://frotafroteq.bubbleapps.io/api/1.1/obj/acompanhamentoFrota')
    dados_dic_tt = dados_api_tt.json()
    df_tt = pd.DataFrame(dados_dic_tt['response']['results'])
    df_tt = df_tt[['Motorista','Prefixo','Status','Tipo de Equipamento','Origem x Destino','Cidade Atual','Atendimento','Chegada (Origem)','Saída (Origem)','Chegada (Destino)','Observação_VIX']]
    df_tt['Chegada (Origem)'] = pd.to_datetime(df_tt['Chegada (Origem)'])
    df_tt['Saída (Origem)'] = pd.to_datetime(df_tt['Saída (Origem)'])
    df_tt['Chegada (Destino)'] = pd.to_datetime(df_tt['Chegada (Destino)'])
    return df_tt
@st.cache_data
def carregar_dados_poli():
    dados_api_poli = requests.get('https://frotafroteq.bubbleapps.io/api/1.1/obj/acompanhamentopoli')
    dados_dic_poli = dados_api_poli.json()
    df_poli = pd.DataFrame(dados_dic_poli['response']['results'])
    df_poli = df_poli[['Motorista','Cavalo Texto','Status','Tipo Equipamento','Local','Atendimento Texto','Origem x Destino','Chegada (Origem)','Saída (Origem)','Chegada (Destino)','Observação_VIX']]
    df_poli['Chegada (Origem)'] = pd.to_datetime(df_tt['Chegada (Origem)'])
    df_poli['Saída (Origem)'] = pd.to_datetime(df_tt['Saída (Origem)'])
    df_poli['Chegada (Destino)'] = pd.to_datetime(df_tt['Chegada (Destino)'])
    return df_poli

df_tt = carregar_dados_tt()
df_poli = carregar_dados_poli()

#Tratamento dados do TT
op_status_tt = df_tt.Status.unique().tolist()
op_cidade_tt = df_tt['Cidade Atual'].unique().tolist()
op_tipo_tt = df_tt['Tipo de Equipamento'].unique().tolist()
op_status_tt.append('Todos')
op_tipo_tt.append('Todos')
op_cidade_tt.append('Todos')

#Tratamento POLI
op_status_poli = df_poli.Status.unique().tolist()
op_cidade_poli = df_poli['Local'].unique().tolist()
op_tipo_poli = df_poli['Tipo Equipamento'].unique().tolist()
op_status_poli.append('Todos')
op_tipo_poli.append('Todos')
op_cidade_poli.append('Todos')


#Container TT
with st.container():
    st.subheader('Frota TT')
    col1, col2 = st.columns(2)
    with col1:
        cidade = st.selectbox('Cidade Atual', op_cidade_tt)
    with col2:
        status = st.selectbox('Status da Frota',op_status_tt)
    #tipo = st.selectbox('Status da Frota', op_tipo_tt)

    if cidade =="Todos" and status =="Todos":
        st.dataframe(df_tt[['Motorista', 'Prefixo', 'Tipo de Equipamento', 'Atendimento', 'Origem x Destino','Chegada (Origem)',
                            'Chegada (Destino)', 'Saída (Origem)', 'Observação_VIX']])

    if cidade !="Todos" and status !="Todos":
        df_tt = df_tt[(df_tt['Status'] == status) & (df_tt['Cidade Atual'] == cidade)]
        st.dataframe(df_tt[['Motorista', 'Prefixo', 'Tipo de Equipamento', 'Atendimento','Origem x Destino', 'Chegada (Origem)',
                            'Chegada (Destino)', 'Saída (Origem)', 'Observação_VIX']])

    if cidade =="Todos" and status !="Todos":
        df_tt = df_tt[(df_tt['Status'] == status)]
        st.dataframe(df_tt[['Motorista', 'Prefixo', 'Tipo de Equipamento', 'Atendimento','Origem x Destino', 'Chegada (Origem)',
                            'Chegada (Destino)', 'Saída (Origem)', 'Observação_VIX']])

    if status =="Todos" and cidade !="Todos":
        df_tt = df_tt[(df_tt['Cidade Atual'] == cidade)]
        st.dataframe(df_tt[['Motorista', 'Prefixo', 'Tipo de Equipamento', 'Atendimento','Origem x Destino' ,'Chegada (Origem)',
                            'Chegada (Destino)', 'Saída (Origem)', 'Observação_VIX']])

#Container poli macae
with st.container():
    st.subheader('Frota POLI MACAÉ')
    col1, col2 = st.columns(2)
    with col1:
        cidade_poli = st.selectbox('Cidade Atual', op_cidade_poli)
    with col2:
        status_poli = st.selectbox('Status da Frota',op_status_poli)
    #tipo = st.selectbox('Status da Frota', op_tipo_poli)

    if cidade_poli =="Todos" and status_poli =="Todos":
        st.dataframe(df_poli[['Motorista', 'Cavalo Texto', 'Tipo Equipamento', 'Atendimento Texto','Origem x Destino', 'Chegada (Origem)',
                            'Chegada (Destino)', 'Saída (Origem)', 'Observação_VIX']])

    if cidade_poli !="Todos" and status_poli !="Todos":
        df_poli = df_poli[(df_poli['Status'] == status_poli) & (df_poli['Local'] == cidade_poli)]
        st.dataframe(df_poli[['Motorista', 'Cavalo Texto', 'Tipo Equipamento', 'Atendimento Texto','Origem x Destino', 'Chegada (Origem)',
                              'Chegada (Destino)', 'Saída (Origem)', 'Observação_VIX']])

    if cidade_poli =="Todos" and status_poli !="Todos":
        df_poli = df_poli[(df_poli['Status'] == status_poli)]
        st.dataframe(df_poli[['Motorista', 'Cavalo Texto', 'Tipo Equipamento', 'Atendimento Texto','Origem x Destino', 'Chegada (Origem)',
                              'Chegada (Destino)', 'Saída (Origem)', 'Observação_VIX']])

    if status_poli =="Todos" and cidade_poli !="Todos":
        df_poli = df_poli[(df_poli['Local'] == cidade_poli)]
        st.dataframe(df_poli[['Motorista', 'Cavalo Texto', 'Tipo Equipamento', 'Atendimento Texto','Origem x Destino', 'Chegada (Origem)',
                              'Chegada (Destino)', 'Saída (Origem)', 'Observação_VIX']])
