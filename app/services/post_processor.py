"""
app/services/post_processor.py - Post-generation validation and enforcement.
"""

from config import settings


class PostProcessor:
    """Validates and enforces platform constraints on generated content."""

    @staticmethod
    def enforce_character_limit(text: str, platform: str) -> str:
        """Truncates text to platform character limit if needed."""
        limit = settings.PLATFORM_LIMITS.get(platform, 500)
        if len(text) > limit:
            return text[:limit - 3] + "..."
        return text

    @staticmethod
    def enforce_hashtag_limit(hashtags: list, platform: str) -> list:
        """Limits hashtags to platform maximum."""
        limit = settings.HASHTAG_LIMITS.get(platform, 3)
        return hashtags[:limit]

    @staticmethod
    def ensure_cta(text: str, cta: str) -> str:
        """Ensures CTA is present in the post text."""
        if cta.lower() not in text.lower():
            text += f"\n\n{cta}"
        return text

    @classmethod
    def process(cls, text: str, hashtags: list, platform: str, cta: str) -> dict:
        """Runs all post-processing steps and returns cleaned content."""
        text = cls.enforce_character_limit(text, platform)
        hashtags = cls.enforce_hashtag_limit(hashtags, platform)
        text = cls.ensure_cta(text, cta)

        return {
            "post_text": text,
            "hashtags": hashtags,
            "character_count": len(text),
            "cta": cta,
        }