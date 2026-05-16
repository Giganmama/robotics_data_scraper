import scrapy
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CatalogSpider(scrapy.Spider):
    name = "catalog"
    # Пример источника (можно заменить на любой публичный каталог датасетов)
    start_urls = ["https://paperswithcode.com/sota"] 
    
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "USER_AGENT": "Mozilla/5.0 (Robotics-Data-Scraper/1.0)",
    }

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        # Адаптируй селекторы под реальный сайт
        items = soup.select(".dataset-item, .card, .row") 

        for item in items:
            try:
                title_el = item.select_one("h3, .title, a")
                link_el = item.select_one("a")
                
                title = title_el.get_text(strip=True) if title_el else "Unknown"
                link = urljoin(response.url, link_el["href"]) if link_el else None
                
                tags = [t.get_text(strip=True) for t in item.select(".tag, .badge")]
                
                yield {
                    "title": title,
                    "url": link,
                    "tags": tags,
                    "source": response.url,
                    "scraped_at": response.headers.get("Date", "").decode()
                }
            except Exception as e:
                logger.warning(f"Parse error: {e}")

        # Пагинация (пример)
        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
