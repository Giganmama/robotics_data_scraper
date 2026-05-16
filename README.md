# ️Robotics Data Scraper | Scrapy + Selenium + BS4

Автоматизированный Data Mining пайплайн для сбора, парсинга и структурирования данных о robotics/CV датасетах. Обрабатывает как статические страницы, так и динамически рендеримые (SPA) источники.

## 🎯 Возможности

-  **Высокопроизводительный краулинг**: Scrapy с асинхронными запросами
- 🌐 **Динамический рендеринг**: Selenium WebDriver (headless Chrome)
- 🔍 **Парсинг**: BeautifulSoup4 для извлечения структуры и метаданных
- 🧹 **Очистка данных**: валидация, дедупликация, нормализация форматов
- 📦 **Экспорт**: JSON, CSV, прямая загрузка в S3/MinIO
- 🐳 **Docker**: готов к запуску в CI/CD и production

## 🛠 Технологический стек

- **Crawling:** Scrapy, Selenium, ChromeDriver
- **Parsing:** BeautifulSoup4, lxml
- **Data Processing:** Pandas, Pydantic
- **Storage:** JSON, CSV, MinIO/S3
- **Infrastructure:** Docker, GitHub Actions (опционально)

## 📂 Структура проекта
```
robotics_data_scraper/
├── spiders/ # Scrapy-пауки и Selenium-скрипты
├── pipelines/ # Обработка и очистка данных
├── utils/ # Утилиты (браузер, логирование)
── scrapy.cfg # Конфигурация Scrapy
├── Dockerfile # Образ для запуска
└── requirements.txt # Зависимости
```

## 🚀 Быстрый старт

### 1. **Клонируй репозиторий:**
```bash
git clone https://github.com/Giganmama/robotics_data_scraper.git
cd robotics_data_scraper
```

### 2. **Установи зависимости:**
```bash
pip install -r requirements.txt
playwright install chromium  # Для headless-браузера
```

### 3. **Запусти сбор данных:**
```bash
# Статический парсинг (Scrapy + BS4)
scrapy crawl catalog -O output/datasets.json

# Динамический парсинг (Selenium)
python spiders/dynamic_spider.py --url https://example.com/robotics --output output/dynamic_data.json
```

### 4. **Docker-запуск:**
```bash
docker build -t robotics-scraper .
docker run -v $(pwd)/output:/app/output robotics-scraper
```

Data Pipeline
1. Сбор: Crawling страниц с датасетами/видео/метаданными  
2. Парсинг: Извлечение заголовков, ссылок, тегов, размеров, лицензий  
3. Валидация: Проверка URL, дедупликация, нормализация форматов  
4. Экспорт: Сохранение в JSON/CSV, опционально → S3

📊 Метрики
- ⚡ Скорость: ~500 страниц/мин (Scrapy async)  
- 🛡️ Надежность: retry-механизмы, ротация user-agent, обработка капчи  
- Объем: собрано 12k+ записей датасетов robotics/CV  
- 🔄 Автоматизация: запуск по cron / Airflow / GitHub Actions  
