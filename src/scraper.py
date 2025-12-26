import asyncio
from crawl4ai import AsyncWebCrawler

async def scrape_website(url: str) -> str:
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        if result.success:
            return result.markdown
        else:
            raise Exception(f"Sayfa çekilemedi: {result.error_message}")