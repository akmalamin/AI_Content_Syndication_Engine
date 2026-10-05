"""app/schemas/content_schema.py - Pydantic models for content generation."""

from pydantic import BaseModel, Field
from typing import List, Optional


class ContentGenerationRequest(BaseModel):
    topic: str = Field(
        ..., min_length=3, max_length=500,
        example="The future of AI in healthcare"
    )
    platforms: List[str] = Field(
        default=["linkedin", "twitter", "newsletter"],
        example=["linkedin", "twitter", "newsletter"],
        description="Target platforms: twitter, linkedin, instagram, newsletter, facebook_ad"
    )
    brand_voice: str = Field(
        default="professional",
        example="professional",
        description="Voice profile: professional, casual, provocative, educational"
    )
    brand_name: str = Field(default="Acme Corp", example="Acme Corp")
    target_audience: str = Field(
        default="CTOs at Series B startups",
        example="CTOs at Series B startups"
    )
    cta: str = Field(
        default="Book a free demo at acmecorp.com/demo",
        example="Book a free demo at acmecorp.com/demo"
    )


class ContentPiece(BaseModel):
    platform: str
    post_text: str
    hashtags: List[str]
    character_count: int
    cta: str
    best_post_time: str
    brand_voice_used: str


class ContentPackageResponse(BaseModel):
    source_topic: str
    brand_voice: str
    total_pieces_generated: int
    content_pieces: List[ContentPiece]
    execution_time_ms: float
    generation_mode: str = Field(..., example="LLM Live" )


class VoiceProfileResponse(BaseModel):
    voice_name: str
    tone: str
    avoid: str
    sentence_style: str