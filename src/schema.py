from pydantic import BaseModel, Field
from typing import List, Optional

class ScrapedData(BaseModel):
    title: str = Field(description="İçeriğin veya ürünün başlığı")
    price: Optional[str] = Field(default=None, description="Varsa fiyat bilgisi")
    summary: str = Field(description="İçeriğin kısa özeti veya açıklaması")
    tags: List[str] = Field(default=[], description="İçerikle ilişkili etiketler veya kategoriler")

