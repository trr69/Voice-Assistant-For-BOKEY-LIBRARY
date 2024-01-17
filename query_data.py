import argparse
from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import API_KEY
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """

это контекст:
---

{context}

---

Отвечай только добротой, вот вопрос: {question}
"""
def user_ask(query_text):
    string_without_magnus = query_text.replace("магнус", "")
    embedding_function = OpenAIEmbeddings(openai_api_key=API_KEY)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    results = db.similarity_search_with_relevance_scores(string_without_magnus, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=string_without_magnus)
    model = ChatOpenAI(openai_api_key=API_KEY)
    response_text = model.predict(prompt)
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    return response_text



