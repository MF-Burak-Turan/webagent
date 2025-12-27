import asyncio
import json
import time
from src.scraper import scrape_website
from src.agent import WebAgent

async def main():
    # Başlangıç zamanını tut
    start_time = time.time()
    
    url = input("\nURL: ")
    query = input("Sorgu: ")
    
    if not url.startswith("http"):
        print("❌ Hata: Geçerli bir URL girmelisiniz!")
        return

    input_prompts = [query]
    
    try:
        crawl_result = await scrape_website(url)
        markdown_content = crawl_result.markdown if hasattr(crawl_result, 'markdown') else str(crawl_result)
        safe_content = markdown_content[:12000]

        agent = WebAgent()
        result = agent.process_content(markdown_content, query)
        
        end_time = time.time()
        execution_seconds = int(end_time - start_time)
        minutes = execution_seconds // 60
        seconds = execution_seconds % 60
        formatted_time = f"{minutes:02d}:{seconds:02d}"

        items_data = [f"{item.title}: {item.value}" for item in result.items]

        output_json = {
            "team_name": "In Frames", 
            "task_id": 2,
            "input_prompts": input_prompts,
            "execution_time": formatted_time,
            "result_output": {
                "summary": result.summary,
                "data": items_data  
            }
        }

        print("\n" + "="*50)
        print(json.dumps(output_json, indent=4, ensure_ascii=False))
        print("="*50)

    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {e}")

if __name__ == "__main__":
    asyncio.run(main())