import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

class ExtractedItem(BaseModel):
    title: str = Field(description="Bulunan öğenin adı, başlığı veya ana etiketi (Örn: Ürün adı, Otel adı, Stok kodu)")
    value: Optional[str] = Field(default="Belirtilmemiş", description="Öğeyle ilgili temel değer veya durum (Örn: Fiyat, Stok Durumu, Tarih, Puan)")
    description: Optional[str] = Field(default="Bilgi yok", description="Öğe hakkında kısa ek açıklama veya konum bilgisi")
    tags: List[str] = Field(default_factory=list, description="Öne çıkan özellikler veya etiketler (Örn: 'İndirimde', 'Lüks', 'Mevcut')")

class GeneralExtractionResult(BaseModel):
    items: List[ExtractedItem] = Field(description="Kullanıcı sorgusuna göre çekilen verilerin listesi")
    summary: str = Field(description="Web sayfasının genel içeriği ve bulunan veriler hakkında kısa bir özet")

class WebAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL"),
            api_key=os.getenv("API_KEY"),
            model=os.getenv("MODEL_NAME"),
        )
        self.structured_llm = self.llm.with_structured_output(GeneralExtractionResult)

    def process_content(self, markdown_content: str, user_query: str):
        system_prompt = f"""
        Sen profesyonel bir web scraping asistanısın. Görevin, sana verilen web içeriğinden 
        kullanıcının isteğine uygun verileri titizlikle ayıklamak ve yapılandırmaktır.
        
        Kullanıcı Ne İstiyor?: "{user_query}"
        
        TALİMATLAR:
        1. SADECE kullanıcı sorgusuyla doğrudan alakalı olan öğeleri çıkar.
        2. Fiyat, sayı veya stok durumu gibi verilerde tam rakamı al (Örn: '7' değil '7.500 TL').
        3. Eğer 'title' (başlık) bilgisini bulamıyorsan o öğeyi listeye ekleme.
        4. Web sayfasındaki gürültüleri (menüler, footer, reklamlar) yoksay.
        5. Eğer kullanıcı belirli bir kriter (örn: 'stokta olanlar') verdiyse bu filtreye sadık kal.
        6. Bu fiyatın {user_query} kriterine matematiksel olarak uyup uymadığını KONTROL ET.
        """
        
        return self.structured_llm.invoke([
            ("system", system_prompt),
            ("user", f"Web İçeriği:\n\n{markdown_content}")
        ])