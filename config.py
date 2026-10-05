"""config.py - Platform limits, brand voice profiles & API configuration."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

    PROJECT_NAME: str = "AI Content Syndication Engine"
    API_V1_STR: str = "/api/v1/content"
    VERSION: str = "1.0.0"
    DOCS_URL: str = "/docs"

    APP_ENV: str = "development"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    DEFAULT_BRAND_VOICE: str = "professional"
    MAX_CONTENT_PIECES: int = 12

    # Platform character limits
    PLATFORM_LIMITS: dict = {
        "twitter": 280,
        "linkedin": 3000,
        "instagram": 2200,
        "newsletter": 5000,
        "facebook_ad": 1000,
    }

    # Hashtag limits per platform
    HASHTAG_LIMITS: dict = {
        "twitter": 2,
        "linkedin": 5,
        "instagram": 20,
        "newsletter": 0,
        "facebook_ad": 3,
    }

    # Brand voice profiles
    VOICE_PROFILES: dict = {
        "professional": {
            "tone": "formal, data-driven, authoritative",
            "avoid": "slang, emojis, exclamation marks",
            "sentence_style": "long, complex, industry-specific",
        },
        "casual": {
            "tone": "friendly, conversational, relatable",
            "avoid": "jargon, passive voice, corporate speak",
            "sentence_style": "short, punchy, emojis allowed",
        },
        "provocative": {
            "tone": "bold, opinionated, attention-grabbing",
            "avoid": "hedging, qualifiers, weak language",
            "sentence_style": "short, direct, challenging",
        },
        "educational": {
            "tone": "informative, helpful, trustworthy",
            "avoid": "sales language, hype, exaggeration",
            "sentence_style": "clear, structured, example-driven",
        },
    }

    @property
    def is_mock_mode(self) -> bool:
        return not self.OPENAI_API_KEY or "your_openai_key" in self.OPENAI_API_KEY


settings = Settings()