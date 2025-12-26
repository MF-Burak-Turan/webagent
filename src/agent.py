import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .schema import ScrapedData

load_dotenv()

class WebAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL"),
            api_key="ollama",
            model=os.getenv("MODEL_NAME"),
        )
        
        self.structured_llm = self.llm.with_structured_output(ScrapedData)
        
    def process_content(self, content: str) -> ScrapedData:
        prompt = (
            "Aşağıdaki web içeriğini analiz et ve başlık, fiyat (varsa), kısa özet ve etiketler şeklinde yapılandırılmış veri olarak döndür.\n\n"
            f"İçerik:\n{content}\n\n"
            "Yapılandırılmış veri formatı:\n"
            "- title: İçeriğin veya ürünün başlığı\n"
            "- price: Varsa fiyat bilgisi\n"
            "- summary: İçeriğin kısa özeti veya açıklaması\n"
            "- tags: İçerikle ilişkili etiketler veya kategoriler (liste halinde)\n"
        )
        return self.structured_llm.invoke(prompt)