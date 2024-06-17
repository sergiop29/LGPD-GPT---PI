from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter


def process_file(files):
    text = ""
    for file in files:
        pdf = PdfReader(file)

        for page in pdf.pages:
            PdfReader(file)
            text += page.extract_text()
    print('----------- A função process_file retornou: ', text)
    return text


def create_text_chunks(text):
    print("MOSTRA AIIIIIIIIIIIIIII", text)
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=3000,
        chunk_overlap=600,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    # print('----------- A função create_text_chunks retornou: ', chunks)
    return chunks
