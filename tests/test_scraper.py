import pytest
from src.scraper import scrape_website

@pytest.mark.asyncio
async def test_scrape_website():
    url = "https://example.com"
    content = await scrape_website(url)
    assert isinstance(content, str)
    assert len(content) > 0
    assert "Example Domain" in content