"""
app/services/prompt_builder.py - Platform-specific prompt template engine.

Constructs structured prompts that force the LLM to generate
platform-optimized content with correct formatting, length, and tone.
"""

from config import settings


class PromptBuilder:
    """Builds platform-specific generation prompts with brand voice injection."""

    PLATFORM_FORMATS = {
        "twitter": {
            "format": "Punchy hook (under 280 chars). Start with a bold statement or question. "
                      "Use 1-2 hashtags max. End with a short CTA.",
            "example": "AI in healthcare isn't coming. It's already here.\n\n"
                       "5 ways it's changing patient outcomes:\n"
                       "1. Faster diagnosis\n2. Drug discovery\n3. Personalized treatment\n\n"
                       "Which one excites you most? 👇\n\n#AI #HealthTech",
        },
        "linkedin": {
            "format": "Professional long-form post (800-1,300 chars). "
                      "Start with a hook line, then a line break. "
                      "Share a problem, then an insight. End with a question CTA. "
                      "Add 3-5 hashtags at the bottom.",
            "example": "Most CTOs are underestimating AI's impact on healthcare.\n\n"
                       "Last quarter, we analyzed 500 patient workflows...\n\n"
                       "[Insight paragraph]\n\n"
                       "What's your biggest AI challenge? Comment below.\n\n"
                       "#AI #Healthcare #DigitalTransformation #CTO #Innovation",
        },
        "instagram": {
            "format": "Visual-first caption (500-1,000 chars). "
                      "Start with an emoji hook. Tell a mini-story. "
                      "Add value. End with a CTA. "
                      "Add 15-20 hashtags in a block at the end.",
            "example": "🚀 This one AI tool saved our clinic 20 hours/week...\n\n"
                       "[Story paragraph]\n\n"
                       "Save this post for later! 💾\n\n"
                       "#AI #Healthcare #DigitalHealth #MedTech ...",
        },
        "newsletter": {
            "format": "Email newsletter format (300-500 words). "
                      "Include a subject line, preview text, greeting, "
                      "body with 2-3 key points, and a CTA button text.",
            "example": "Subject: The AI revolution in healthcare is here\n"
                       "Preview: 5 ways AI is transforming patient care...\n\n"
                       "Hi [First Name],\n\n"
                       "[Body paragraphs]\n\n"
                       "[CTA Button: Book Your Free Demo]",
        },
        "facebook_ad": {
            "format": "Facebook ad copy (100-300 chars primary text). "
                      "Start with a pain point. State the solution. "
                      "End with a strong CTA. Keep it punchy.",
            "example": "Tired of spending 10 hours/week on manual reports?\n\n"
                       "Our AI cuts reporting time by 80%.\n\n"
                       "👉 Try it free for 14 days.",
        },
    }

    @classmethod
    def build_prompt(cls, topic: str, platform: str, voice_name: str,
                     brand_name: str, target_audience: str, cta: str) -> str:
        """Constructs a complete generation prompt for a specific platform."""

        voice = settings.VOICE_PROFILES.get(voice_name, settings.VOICE_PROFILES["professional"])
        char_limit = settings.PLATFORM_LIMITS.get(platform, 500)
        hashtag_limit = settings.HASHTAG_LIMITS.get(platform, 3)
        fmt = cls.PLATFORM_FORMATS.get(platform, cls.PLATFORM_FORMATS["linkedin"])

        prompt = f"""You are a world-class content strategist writing for {brand_name}.

BRAND VOICE: {voice['tone']}
AVOID: {voice['avoid']}
SENTENCE STYLE: {voice['sentence_style']}

TARGET AUDIENCE: {target_audience}
PLATFORM: {platform.upper()}
CHARACTER LIMIT: {char_limit} characters MAXIMUM
HASHTAG LIMIT: {hashtag_limit} hashtags maximum
CALL TO ACTION: {cta}

TOPIC: {topic}

FORMAT INSTRUCTIONS:
{fmt['format']}

EXAMPLE OF GOOD OUTPUT:
{fmt['example']}

RULES:
1. Your output MUST be under {char_limit} characters.
2. Include exactly {hashtag_limit} hashtags (if applicable).
3. Include the CTA: "{cta}"
4. Do NOT fabricate statistics or fake citations.
5. Write ONLY the post content. No explanations or meta-commentary.

Generate the {platform} post now:"""

        return prompt