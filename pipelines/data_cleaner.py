import pandas as pd
import logging
from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetRecord(BaseModel):
    title: str
    url: HttpUrl
    tags: Optional[List[str]] = []
    source: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

class DataCleaner:
    def __init__(self):
        self.seen_urls = set()

    def clean_and_validate(self, records: List[dict]) -> List[dict]:
        cleaned = []
        for rec in records:
            try:
                validated = DatasetRecord(**rec)
                url_str = str(validated.url)
                if url_str not in self.seen_urls:
                    self.seen_urls.add(url_str)
                    cleaned.append(validated.model_dump())
            except Exception as e:
                logger.warning(f"Validation failed: {e}")
        return cleaned

    def to_csv(self, records: List[dict], path: str = "output/cleaned_datasets.csv"):
        df = pd.DataFrame(records)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        logger.info(f"Exported {len(df)} records to {path}")
        return df
