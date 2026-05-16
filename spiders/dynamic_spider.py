import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamicScraper:
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def scrape(self, url: str, output_path: str = "output/dynamic_data.json"):
        logger.info(f"Loading dynamic page: {url}")
        self.driver.get(url)
        
        # Ждем рендеринга
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        data = []
        # Пример поиска элементов
        items = self.driver.find_elements(By.CSS_SELECTOR, ".item, .card, .dataset-row")
        
        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, "h3, .title, a").text
                link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                data.append({"title": title, "url": link, "type": "dynamic"})
            except Exception as e:
                logger.debug(f"Skip item: {e}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(data)} records to {output_path}")
        return data

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", default="output/dynamic_data.json")
    args = parser.parse_args()
    
    scraper = DynamicScraper()
    try:
        scraper.scrape(args.url, args.output)
    finally:
        scraper.close()
