import asyncio
from src.scraper import scrape_website
from src.agent import WebAgent

async def main():
    url = input("\nURL: ")
    query = input("Bu sayfada neyi bulmak/takip etmek istiyorsunuz? \n(Örn: 'Fiyatı 20.000 TL altındaki laptoplar'): ")
    
    if not url.startswith("http"):
        print("❌ Hata: Geçerli bir URL girmelisiniz!")
        return

    print(f"\n[1/2] 🔍 Sayfa içeriği çekiliyor: {url}...")
    
    try:
        crawl_result = await scrape_website(url)
        markdown_content = crawl_result.markdown if hasattr(crawl_result, 'markdown') else crawl_result

        print("[2/2] 🤖 Yapay zeka verileri analiz ediyor...")
        
        agent = WebAgent()
        result = agent.process_content(markdown_content, query)
        
        print("\n" + "="*50)
        print(f"📝 ÖZET: {result.summary}") 
        print("="*50)

        if not result.items:
            print("Sorgunuza uygun ürün bulunamadı.")
        else:
            for i, item in enumerate(result.items, 1):
                print(f"\n{i}. {item.title.upper()}")
                print(f"   📊 Durum/Değer: {item.value}")
                
                if item.description and item.description != "Bilgi yok":
                    print(f"   ℹ️  Açıklama: {item.description}")
                
                if item.tags:
                    print(f"   🏷️  Etiketler: {', '.join(item.tags)}")

        print("\n" + "="*50)

    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {e}")

if __name__ == "__main__":
    asyncio.run(main())