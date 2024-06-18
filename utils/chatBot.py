import os
import shutil
import streamlit as st
import replicate
from langchain_openai.embeddings import OpenAIEmbeddings
# from langchain_community.embeddings import HuggingFaceInstructEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# from langchain_community.llms import CTransformers
from langchain_community.llms import HuggingFaceHub
# from langchain_community.llms import Ollama
# from langchain_community.embeddings import OllamaEmbeddings

load_dotenv()  # Isso carrega as variáveis de ambiente do arquivo .env

def deletar_vectorstore(caminho_pasta):
    try:
        shutil.rmtree(caminho_pasta)
        # print("Pasta deletada com sucesso!")
    except FileNotFoundError:
        print(f"Erro: A pasta '{caminho_pasta}' não foi encontrada.")

def create_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    try:
        vectorstore = FAISS.load_local('vectorstore', embeddings, allow_dangerous_deserialization=True)
        # print('------- Carregou a VECTORSTORE original ', vectorstore)
        new_vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings) # erro aqui
        # print('--------------- Nova Vectorstore!@!!!!! ', new_vectorstore)
        new_vectorstore.save_local("vectorstore_2")
        new_vectorstore = FAISS.load_local("vectorstore_2", embeddings, allow_dangerous_deserialization=True)
        # print('--------------- Nova Vectorstore_2!!!!!! ', vectorstore_2)
        vectorstore.merge_from(new_vectorstore)
        vectorstore.save_local("vectorstore")
        # print('--------------- Vectorstore MERGEADA ', vectorstore)
        deletar_vectorstore("vectorstore_2")
    except:
        # print("------- rodou except")
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings) # e aqui
        vectorstore.save_local("vectorstore")
        vectorstore = FAISS.load_local('vectorstore', embeddings, allow_dangerous_deserialization=True)

    return vectorstore


# O none aqui deixa o artributo como opcional
def create_conversation_chain(vectorstore=None):
    if (not vectorstore):
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(
            'vectorstore', embeddings, allow_dangerous_deserialization=True)

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.7)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# def generate_llama2_response(prompt_input):
#     string_dialogue = "Use apenas português brasileiro e responda perguntas apenas sobre a LGPD (Lei Geral de Proteção de Dados) e seguranças de dados. Caso receba uma pergunta sobre outro tema, informe que nao poderá responder."
#     for dict_message in st.session_state.messages:
#         if dict_message["role"] == "user":
#             string_dialogue += "User: " + dict_message["content"] + "\n\n"
#         else:
#             string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
#     output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
#                            input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
#                                   "temperature":0.5, "top_p":0.9, "max_length":2000, "repetition_penalty":1})
#     return output

def create_conversation_chain_multi_model(llm_model, vectorstore=None):
    if llm_model == "Chat GPT 3.5":
        llm = ChatOpenAI(
                model="gpt-3.5-turbo-0125", 
                temperature=0.7
                )
        embeddings = OpenAIEmbeddings()

    elif llm_model == "Llama2 13B":
        llm = HuggingFaceHub(
            repo_id = "TheBloke/Llama-2-7B-Chat-GGML",
            model_kwargs = {
                "temperature":0.3,
                "max_length":512
            }
        )
        # llm = CTransformers(
        #         model = "llama-2-7b-chat.ggmlv3.q8_0.bin",
        #         model_type="llama",
        #         max_new_tokens = 512,
        #         temperature = 0.5
        #         )
        embeddings = OpenAIEmbeddings()
        # embeddings = HuggingFaceEmbeddings(
        #                 model_name='sentence-transformers/all-MiniLM-L6-v2', 
        #                 model_kwargs={'device': 'cpu'}
        #                 )

    if (not vectorstore):
        vectorstore = FAISS.load_local(
            'vectorstore', embeddings, allow_dangerous_deserialization=True)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain
