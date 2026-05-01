import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title='Beecrowd Report', page_icon='📊', layout="wide")

@st.cache_data
def carregar_dados(file_uploaded):
    df = pd.read_csv(file_uploaded, sep=";")
    
    # Preenche valores nulos em nomes para evitar erros e cria o Nome Completo
    df['first name'] = df['first name'].fillna('')
    df['sur name'] = df['sur name'].fillna('')
    df['Nome Completo'] = df['first name'] + ' ' + df['sur name']
    
    # Função para definir o perfil do estudante
    def definir_perfil(row):
        resolvidas = row['solved']
        tentadas = row['tried (but not solved)']
        
        if resolvidas >= 6:
            return "Aprovados"
        elif 4 <= resolvidas <= 5:
            return "Quase lá"
        elif resolvidas == 0 and tentadas == 0:
            return "Nem tentou"
        else:
            return "Começou mas desistiu"
            
    df['Perfil'] = df.apply(definir_perfil, axis=1)
    return df

def main():
    st.title('📊 Análise de Desempenho de Estudantes no Beecrowd')

    st.write('Bem-vindo! Este painel analisa o desempenho dos estudantes em desafios de programação.')
    st.write('Carregue um arquivo CSV exportado do Beecrowd e escolha os filtros abaixo.')

    # --- ÁREA DE UPLOAD ---
    st.subheader("📁 Envio de Dados")
    file_uploaded = st.file_uploader("Faça o upload do arquivo CSV com os resultados", type=["csv"])

    if file_uploaded is None:
        st.info("👆 Por favor, envie o arquivo CSV para visualizar o painel.")
        return
    
    try:
        df = carregar_dados(file_uploaded)
    except FileNotFoundError:
        st.error("O arquivo 'desafio - results.csv' não foi encontrado na pasta. Por favor, verifique.")
        return

    # --- MÉTRICAS GERAIS ---
    total_estudantes = len(df)
    
    st.header("1. Visão Geral")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    contagem_perfis = df['Perfil'].value_counts()
    
    col1.metric("Total de Estudantes", total_estudantes)
    col2.metric("Aprovados", contagem_perfis.get("Aprovados", 0))
    col3.metric("Quase lá", contagem_perfis.get("Quase lá", 0))
    col4.metric("Começou mas desistiu", contagem_perfis.get("Começou mas desistiu", 0))
    col5.metric("Nem tentou", contagem_perfis.get("Nem tentou", 0))

    st.divider()

    # --- GRÁFICOS ---
    st.header("2. Análise Visual")
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        # Gráfico de Pizza para percentual
        fig_pie = px.pie(
            df, 
            names='Perfil', 
            title='Distribuição dos Perfis de Estudantes (%)',
            color='Perfil',
            color_discrete_map={
                'Aprovados': '#28a745',
                'Quase lá': '#ffc107',
                'Começou mas desistiu': '#fd7e14',
                'Nem tentou': '#dc3545'
            },
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_graf2:
        # Gráfico de Barras: Média de pontuação (score) por perfil
        media_score = df.groupby('Perfil', as_index=False)['score'].mean()
        fig_bar = px.bar(
            media_score, 
            x='Perfil', 
            y='score', 
            title='Média de Pontuação por Perfil',
            labels={'score': 'Pontuação Média (Score)', 'Perfil': 'Perfil do Estudante'},
            color='Perfil',
            text_auto='.2f'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- RELATÓRIOS E FILTROS ---
    st.header("3. Relatórios Detalhados")
    st.markdown("Filtre por perfil para visualizar o nome e o email dos estudantes. Você pode exportar os resultados abaixo.")
    
    # Filtro
    perfil_selecionado = st.selectbox("Selecione o perfil que deseja visualizar:", 
                                      options=["Todos", "Aprovados", "Quase lá", "Começou mas desistiu", "Nem tentou"])
    
    # Aplicação do Filtro
    if perfil_selecionado == "Todos":
        df_filtrado = df
    else:
        df_filtrado = df[df['Perfil'] == perfil_selecionado]
        
    # Selecionar apenas as colunas solicitadas para o relatório
    relatorio_df = df_filtrado[['Nome Completo', 'email', 'solved', 'score', 'Perfil']].rename(
        columns={
            'email': 'E-mail',
            'solved': 'Questões Resolvidas',
            'score': 'Pontuação'
        }
    )
    
    st.write(f"Mostrando **{len(relatorio_df)}** estudantes do perfil **{perfil_selecionado}**.")
    st.dataframe(relatorio_df, use_container_width=True, hide_index=True)
    
    # Botão de Exportação para CSV
    csv_dados = relatorio_df.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button(
        label="📥 Baixar Relatório Filtrado (CSV)",
        data=csv_dados,
        file_name=f"relatorio_estudantes_{perfil_selecionado.lower().replace(' ', '_')}.csv",
        mime='text/csv',
    )
    

if __name__ == "__main__":
    main()
