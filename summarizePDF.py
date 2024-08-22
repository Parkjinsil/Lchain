#!/usr/bin/env python
# coding: utf-8

# ### <PDF 요약 웹사이트 만들기>
# PyPDF2 : PDF 파일 읽고, 분할, 병합, 순서 바꾸고, 추가, 암호화 등의 작업 할 수 있게 해주는 라이브러리  
#         파이썬에서 PDF 파일을 처리하기 위한 라이브러리

# In[14]:


# pip install langchain


# In[15]:


# pip install streamlit


# In[16]:


# pip install PyPDF2


# In[17]:


# pip install sentence-transformers


# In[18]:


# pip install PyPDF2


# In[1]:


from PyPDF2 import PdfReader
import streamlit as st 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import FAISS # 고성능 벡터 검색 라이브러리 / 텍스트 청크를 벡터화한 후 검색 수행하는데 사용됨
from langchain.chains.question_answering import load_qa_chain # 질문-응답 체인을 로드하는 데 사용됨
from langchain_community.llms import Ollama

def process_text(text):
    # CharacterTextSplitter를 사용하여 텍스트를 청크로 분할
    text_splitter = CharacterTextSplitter(
        separator='\n',             # 줄바꿈을 기준으로 텍스트 분할
        chunk_size=1000,            # 각 청크의 최대 길이
        chunk_overlap=200,          # 청크 간의 중복되는 부분의 길이
        length_function=len         # 텍스트 길이 계산하는 함수
    )
    chunks = text_splitter.split_text(text) # text를 입력 받아 설정한 대로 청크로 분할

    # 임베딩 처리(벡터 변환), 임베딩은 HuggingFaceEmbeddings 모델을 사용
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    documents = FAISS.from_texts(chunks, embeddings) # 텍스트 청크를 벡터로 변환하고 FAISS db에 저장
    return documents

def main() : # streamlit을 이용한 웹사이트 생성
    st.title('PDF 요약하기')
    st.divider() # 페이지에 구분선 추가

    pdf = st.file_uploader('PDF파일을 업로드해주세용', type='pdf') # 사용자가 PDF 파일을 업로드할 수 있는 위젯 제공

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = '' # 텍스트 변수에 PDF 내용을 저장
        for page in pdf_reader.pages:
            text += page.extract_text()

        documents = process_text(text) # PDF에서 추출한 텍스트를 청크로 분할하고, 벡터화한 후 FAISS db에 저장
        query = '업로드된 PDF 파일의 내용을 약 3~5문장으로 요약해주세요' # LLM에 PDF파일 요약 요청

        if query:
            docs = documents.similarity_search(query) # 쿼리와 가장 유사한 텍스트 청크 찾음
            llm = Ollama(model='llama3')
            chain = load_qa_chain(llm, chain_type='stuff') # 질문-응답 체인 로드/ 유사 문서에서 정보 추출하여 질문에 대한 답변 생성하는 데 사용

            # 질문과 유사 문서를 바탕으로 LLM이 답변 반환
            response = chain.run(input_documents=docs, question=query)

            st.subheader('--요약 결과--') # 요약 결과를 표시할 부분의 제목 설정
            st.write(response) 

if __name__ == '__main__': # 스크립트가 직접 실행될 때 'main()'함수 호출 / import되어 사용될 때와 구분 
    main()



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




