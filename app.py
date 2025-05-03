import streamlit as st


st.set_page_config(page_title='Beecrowd Report', page_icon='📊')

st.title('📊 Análise de Desempenho de Estudantes no Beecrowd')
st.write('Carregue um arquivo CSV exportado do Beecrowd e escolha os filtros abaixo.')

uploaded_file = st.file_uploader(
    'Selecione o arquivo CSV',
    type='csv',
    help='Arquivo exportado do Beecrowd (\';\' como separador).'
)

status_options = {
    'Aprovados': '1',
    'Quase lá': '2',
    'Começou mas desistiu': '3',
    'Nem tentou': '4'
}

selected_labels = st.multiselect(
    'Filtrar candidatos pelos status:',
    options=list(status_options.keys()),
    default=list(status_options.keys())[0]
)

st.write('Status selecionados:', selected_labels)

generate = st.button('Gerar relatório')

if generate:
    if not uploaded_file:
        st.error('⚠️ Por favor, selecione um arquivo CSV primeiro.')
    else:
        st.success('Arquivo recebido! (Processamento virá na próxima fase)')
