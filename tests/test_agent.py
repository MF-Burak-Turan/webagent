from src.agent import WebAgent
from src.schema import ScrapedData

def test_agent_structure():
    agent = WebAgent()
    fake_markdown = "Ürün Başlığı\nFiyat: 99.99 TL\nBu ürün harika bir üründür.\nEtiketler: elektronik, gadget"
    result = agent.process_content(fake_markdown)
    
    assert isinstance(result, ScrapedData)
    assert result.title == "Ürün Başlığı"
    assert result.price == "99.99 TL"    