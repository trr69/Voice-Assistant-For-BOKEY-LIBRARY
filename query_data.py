from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import API_KEY
from decorators import check_time_decorator

class GPTQuery:
    def __init__(self, CHROMA_PATH = "chroma", 
                PROMPT_TEMPLATE = """
                это контекст:
                ---
                {context}
                ---
                Chat History:
                {chat_history}
                ---
                Отвечай только добротой, вот вопрос: {question}
                """ ) -> None:
        self.chat_history = []
        self.__CHROMA_PATH = CHROMA_PATH
        self.__PROMPT_TEMPLATE = PROMPT_TEMPLATE


    @check_time_decorator
    def user_ask(self, query_text):
        string_without_magnus = query_text.replace("магнус", "")

        embedding_function = OpenAIEmbeddings(openai_api_key=API_KEY)

        db = Chroma(persist_directory=self.__CHROMA_PATH, embedding_function=embedding_function)

        results = db.similarity_search_with_relevance_scores(string_without_magnus, k=3)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

        prompt_template = ChatPromptTemplate.from_template(self.__PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=string_without_magnus, chat_history=self.chat_history)
        model = ChatOpenAI(openai_api_key=API_KEY)
        response_text = model.predict(prompt)

        self.chat_history.append((query_text, response_text))

        print(response_text)
        return response_text



