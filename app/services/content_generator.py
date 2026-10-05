"""
app/services/content_generator.py - LLM content generation with deterministic mock fallback.
"""

import hashlib
from typing import List, Dict
from config import settings
from app.services.prompt_builder import PromptBuilder


class ContentGenerator:
    """Generates platform-specific content using LLM or deterministic mock."""

    # Deterministic mock content templates per platform
    MOCK_TEMPLATES = {
        "twitter": {
            "text": "The future of {topic} is closer than you think.\n\n"
                    "3 things most people miss:\n"
                    "1. Speed of adoption\n"
                    "2. Cost reduction\n"
                    "3. Competitive advantage\n\n"
                    "Which one matters most to you?\n\n"
                    "{cta}",
            "hashtags": ["#AI", "#Innovation"],
            "best_time": "Wednesday 12:00 PM EST",
        },
        "linkedin": {
            "text": "Most leaders in {audience} are underestimating the impact of {topic}.\n\n"
                    "Last quarter, we analyzed hundreds of workflows and found a pattern "
                    "that most people miss entirely.\n\n"
                    "The companies winning right now aren't the ones with the biggest budgets. "
                    "They're the ones moving fastest on AI adoption.\n\n"
                    "Here's what we learned:\n\n"
                    "1. Early movers capture 3x market share\n"
                    "2. Automation reduces operational costs by 40%\n"
                    "3. Customer satisfaction jumps 25% with AI-powered support\n\n"
                    "What's your biggest challenge with {topic}? "
                    "I'd love to hear your perspective in the comments.\n\n"
                    "{cta}\n\n"
                    "#AI #DigitalTransformation #Innovation #Leadership #FutureOfWork",
            "hashtags": ["#AI", "#DigitalTransformation", "#Innovation", "#Leadership", "#FutureOfWork"],
            "best_time": "Tuesday 8:00 AM EST",
        },
        "instagram": {
            "text": "🚀 This one insight about {topic} changed everything for us...\n\n"
                    "We spent 6 months testing different approaches and here's what "
                    "actually moved the needle:\n\n"
                    "✅ Automate the repetitive stuff first\n"
                    "✅ Focus on customer experience over features\n"
                    "✅ Measure what matters, ignore vanity metrics\n\n"
                    "Save this post for later! 💾\n\n"
                    "{cta}\n\n"
                    "#AI #Innovation #TechTrends #DigitalTransformation #StartupLife "
                    "#GrowthHacking #Marketing #Business #Entrepreneur #FutureOfWork "
                    "#Technology #Automation #Productivity #Leadership #Strategy "
                    "#DataDriven #MachineLearning #SaaS #ContentMarketing #Growth",
            "hashtags": [
                "#AI", "#Innovation", "#TechTrends", "#DigitalTransformation",
                "#StartupLife", "#GrowthHacking", "#Marketing", "#Business",
                "#Entrepreneur", "#FutureOfWork", "#Technology", "#Automation",
                "#Productivity", "#Leadership", "#Strategy", "#DataDriven",
                "#MachineLearning", "#SaaS", "#ContentMarketing", "#Growth"
            ],
            "best_time": "Thursday 11:00 AM EST",
        },
        "newsletter": {
            "text": "Subject: The {topic} revolution is here — are you ready?\n\n"
                    "Preview: 3 insights that will change how you think about {topic}...\n\n"
                    "Hi there,\n\n"
                    "If you've been watching the {topic} space lately, you know "
                    "things are moving fast. Really fast.\n\n"
                    "Here are the 3 biggest takeaways from our latest research:\n\n"
                    "1. ADOPTION IS ACCELERATING\n"
                    "Companies that adopted AI tools in the last 12 months saw "
                    "a 40% reduction in operational costs.\n\n"
                    "2. CUSTOMER EXPECTATIONS ARE SHIFTING\n"
                    "72% of customers now expect AI-powered support experiences.\n\n"
                    "3. THE WINDOW IS CLOSING\n"
                    "Early movers are capturing 3x the market share of late adopters.\n\n"
                    "The question isn't whether to adopt — it's how fast you can move.\n\n"
                    "{cta}\n\n"
                    "Talk soon,\n"
                    "The {brand} Team",
            "hashtags": [],
            "best_time": "Tuesday 9:00 AM EST",
        },
        "facebook_ad": {
            "text": "Still doing things the old way?\n\n"
                    "{topic} is changing the game for {audience}.\n\n"
                    "Companies using AI-powered tools are cutting costs by 40% "
                    "and growing 3x faster.\n\n"
                    "{cta}",
            "hashtags": ["#AI", "#Growth", "#Innovation"],
            "best_time": "Wednesday 2:00 PM EST",
        },
    }

    @classmethod
    def generate_piece(cls, topic: str, platform: str, voice_name: str,
                       brand_name: str, target_audience: str, cta: str) -> Dict:
        """Generates a single content piece for a specific platform."""

        if not settings.is_mock_mode:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                prompt = PromptBuilder.build_prompt(
                    topic, platform, voice_name, brand_name, target_audience, cta
                )
                response = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=800,
                )
                post_text = response.choices[0].message.content.strip()

                # Extract hashtags from generated text
                import re
                hashtags = re.findall(r"#\w+", post_text)
                char_limit = settings.PLATFORM_LIMITS.get(platform, 500)
                if len(post_text) > char_limit:
                    post_text = post_text[:char_limit - 3] + "..."

                return {
                    "text": post_text,
                    "hashtags": hashtags[:settings.HASHTAG_LIMITS.get(platform, 3)],
                    "best_time": "Tuesday 9:00 AM EST",
                }
            except Exception as e:
                print(f"LLM generation failed: {e}. Using mock fallback.")

        # Deterministic mock generation
        template = cls.MOCK_TEMPLATES.get(platform, cls.MOCK_TEMPLATES["linkedin"])
        post_text = template["text"].format(
            topic=topic,
            audience=target_audience,
            cta=cta,
            brand=brand_name,
        )

        char_limit = settings.PLATFORM_LIMITS.get(platform, 500)
        if len(post_text) > char_limit:
            post_text = post_text[:char_limit - 3] + "..."

        return {
            "text": post_text,
            "hashtags": template["hashtags"][:settings.HASHTAG_LIMITS.get(platform, 3)],
            "best_time": template["best_time"],
        }