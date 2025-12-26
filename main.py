import asyncio
from src.scraper import scrape_website
from src.agent import WebAgent

async def main():
    target_url = input("Çekilecek web sayfasının URL'sini girin: ")

    print("Sayfa çekiliyor...")
    markdown_content = await scrape_website(target_url)
    
    print("İçerik işleniyor...")
    agent = WebAgent()
    result = agent.process_content(markdown_content)
    
    print("\nYapılandırılmış Veri Sonucu:")
    print(result.model_dump_json(indent=4))
    
if __name__ == "__main__":
    asyncio.run(main())