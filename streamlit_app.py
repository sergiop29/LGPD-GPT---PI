import streamlit as st
from utils import chatBot, text
from streamlit_chat import message
from dotenv import load_dotenv
import time
import os
import glob

def main():
    # Início da página e configs
    st.set_page_config(page_title='LGPDNOW GPT', page_icon='utils/lgpd_logo_verde.png', layout="centered")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.empty()
    col2.image('utils/Logo-lgpd-com-nome.png', width=475)
    col3.empty()
    col4.empty()
    col5.empty()
    col6.empty()
    col7.empty()
    st.header(':green[Converse com um especialista em LGPD] 💬')

    with st.sidebar:
        # "Header" do sideabr
        st.header('Seu Chatbot pessoal treinado pela LGPDNOW! ', divider='green')
        st.write("")
        st.caption(""" <p style='text-align:justify'>
        A Lei Geral de Proteção de Dados Pessoais (LGPD) foi promulgada em 2018 com o objetivo de garantir os direitos à liberdade, privacidade e personalidade dos indivíduos. Ela se aplica a qualquer pessoa, seja física ou jurídica, incluindo empresas e órgãos públicos.
    <p style='text-align:justify'>
    A LGPD define regras claras para a coleta, armazenamento, uso e compartilhamento de dados pessoais. Isso significa que você tem mais controle sobre suas informações e pode saber como elas estão sendo utilizadas.
    <p style='text-align:justify'>
    Com a LGPD em vigor desde 2020, empresas e órgãos que não se adequarem à lei podem ser punidos com multas.
        </p>""", unsafe_allow_html=True)
        st.markdown("")

        # Selectbox para modelos de llm
        st.subheader('Escolha o modelo para atendimento')
        selected_model = st.sidebar.selectbox('Modelo', 
                                            options=['Chat GPT 3.5', 
                                                    #'Llama2 13B',
                                                    # 'Mistral',
                                                    ], 
                                            label_visibility = "collapsed"
                                            )
        llm = selected_model

        # Documentos usados no RAG
        st.markdown("")
        st.subheader('Base Legal')
        with st.expander("Legislação utilizada no modelo"):
            # st.write("LEI No 13.709, DE 14 DE AGOSTO DE 2018")
            # st.write("Política de Comunicação Social - ANPD")
            # st.write("Decreto nº 48891 de 2024 - Rio de Janeiro")
            # loop para nomear arquivos para Base Legal
            pdf_files = glob.glob(os.path.join("normas", "*.pdf"))
            for pdf_file in pdf_files:
                filename = os.path.basename(pdf_file)  # Extract filename
                st.write(f"•   {filename}")

        # Botão de "Clear Chat"
        st.markdown("")
        def clear_chat_history():
            st.session_state.messages = []
            # response = ""
            # prompt = ""
        st.sidebar.button('Limpar Chat', on_click=clear_chat_history)
        st.divider()

        # Footer do sidebar
        st.caption("<p style='text-align:center'> Made by LGPDNOW </p>",
                    unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.empty()
        col2.empty()
        col3.image('utils/lgpd_logo_verde.png', width=40)
        col4.empty()
        col5.empty()
        st.markdown("")

    # ------ INICIO HABILITAR O PROCESSAMENTO DE ARQUIVOS PDF ----#

    #     pdf_docs = st.file_uploader(
    #     "Carregue os seus arquivos, em formato PDF, aqui", accept_multiple_files=True)
    #     # print(type(pdf_docs))

    #     if st.button('Processar'):
    #         all_files_text = text.process_file(pdf_docs)

    #         chunks = text.create_text_chunks(all_files_text)

    #         vectorstore = chatBot.create_vectorstore(chunks)
            
    # #         # print('---- vectorstore que aparece no app final HEIN; ', vectorstore)

    # _____ FIM HABILITAR O PROCESSAMENTO DE ARQUIVOS PDF ____#

# ----------------------- PÁGINA PRINCIPAL -----------------------
    # Manter histórico de chat entre sessões
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for i, message in enumerate(st.session_state.messages):
        if (i % 2 == 0):
            with st.chat_message(message["role"], avatar="🧑"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar="utils/lgpd_logo_verde.png"):
                st.markdown(message["content"])

    # Chatbot
    if prompt := st.chat_input("Como posso ajudar?"):
        # Pergunta do usuário
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content":prompt})
        # Inicializar conversa
        st.session_state.conversation = chatBot.create_conversation_chain_multi_model(llm)
        response = st.session_state.conversation(prompt)['chat_history'][1].content
        # Resposta do chatbot
        def stream_data():
            for word in response.split(" "):
                yield word + " "
                time.sleep(0.06)
        with st.chat_message("assistant", avatar="utils/lgpd_logo_verde.png"):
            # st.markdown(response)
            st.write_stream(stream_data)
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == '__main__':

    main()
