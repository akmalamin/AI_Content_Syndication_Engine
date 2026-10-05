"""
app/routers/content_router.py - Content generation, calendar & voice profile endpoints.
"""

import time
from fastapi import APIRouter, HTTPException, status
from typing import List

from config import settings
from app.schemas.content_schema import (
    ContentGenerationRequest,
    ContentPiece,
    ContentPackageResponse,
    VoiceProfileResponse,
)
from app.services.content_generator import ContentGenerator
from app.services.post_processor import PostProcessor

router = APIRouter(prefix="/content", tags=["Content Generation & Syndication"])


@router.post("/generate", response_model=ContentPackageResponse, status_code=status.HTTP_200_OK)
def generate_content_package(request: ContentGenerationRequest):
    """
    Generate a multi-platform content package from a single topic.
    Returns platform-specific posts with hashtags, CTAs, and scheduling metadata.
    """
    start_time = time.perf_counter()

    # Validate brand voice
    if request.brand_voice not in settings.VOICE_PROFILES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid voice '{request.brand_voice}'. "
                   f"Choose from: {list(settings.VOICE_PROFILES.keys())}"
        )

    # Validate platforms
    valid_platforms = list(settings.PLATFORM_LIMITS.keys())
    for p in request.platforms:
        if p not in valid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform '{p}'. Choose from: {valid_platforms}"
            )

    content_pieces = []

    for platform in request.platforms:
        # Generate raw content
        raw = ContentGenerator.generate_piece(
            topic=request.topic,
            platform=platform,
            voice_name=request.brand_voice,
            brand_name=request.brand_name,
            target_audience=request.target_audience,
            cta=request.cta,
        )

        # Post-process (enforce limits, hashtags, CTA)
        processed = PostProcessor.process(
            text=raw["text"],
            hashtags=raw["hashtags"],
            platform=platform,
            cta=request.cta,
        )

        content_pieces.append(ContentPiece(
            platform=platform,
            post_text=processed["post_text"],
            hashtags=processed["hashtags"],
            character_count=processed["character_count"],
            cta=processed["cta"],
            best_post_time=raw["best_time"],
            brand_voice_used=request.brand_voice,
        ))

    elapsed = round((time.perf_counter() - start_time) * 1000, 2)
    mode = "LLM Live (OpenAI)" if not settings.is_mock_mode else "Deterministic Mock (Zero-Cost)"

    return ContentPackageResponse(
        source_topic=request.topic,
        brand_voice=request.brand_voice,
        total_pieces_generated=len(content_pieces),
        content_pieces=content_pieces,
        execution_time_ms=elapsed,
        generation_mode=mode,
    )


@router.get("/voices", response_model=List[VoiceProfileResponse])
def list_voice_profiles():
    """Returns all available brand voice profiles."""
    profiles = []
    for name, config in settings.VOICE_PROFILES.items():
        profiles.append(VoiceProfileResponse(
            voice_name=name,
            tone=config["tone"],
            avoid=config["avoid"],
            sentence_style=config["sentence_style"],
        ))
    return profiles


@router.get("/platforms")
def list_supported_platforms():
    """Returns supported platforms with character and hashtag limits."""
    platforms = {}
    for platform, char_limit in settings.PLATFORM_LIMITS.items():
        platforms[platform] = {
            "character_limit": char_limit,
            "hashtag_limit": settings.HASHTAG_LIMITS.get(platform, 3),
        }
    return {"supported_platforms": platforms}