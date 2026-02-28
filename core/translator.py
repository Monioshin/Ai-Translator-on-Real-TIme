import httpx
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

class AIEngine:
    def __init__(self, api_key, proxy_url=None):
        # Настройка прокси
        client = httpx.Client(proxies=proxy_url) if proxy_url else None
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3,
            http_client=client
        )

    def translate_and_fix(self, text, target_lang="English"):
        prompt = ChatPromptTemplate.from_template(
            "You are a professional translator. Translate this text to {target_lang} "
            "and fix grammar/flow. Return ONLY the translated text.\n\nText: {text}"
        )
        chain = prompt | self.llm
        try:
            response = chain.invoke({"target_lang": target_lang, "text": text})
            return response.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"