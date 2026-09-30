from typing import List
from pydantic import BaseModel, Field


class AIArticleOutput(BaseModel):
    """Structured output expected from the Antigravity/Gemini AI Agent."""
    headline: str = Field(..., description="Compelling and accurate news headline")
    summary: str = Field(..., description="1-2 sentence executive summary of the news story")
    body_content: str = Field(..., description="Detailed news article body formatted with standard HTML (<p>, <strong>, etc.)")
    location: str = Field(..., description="Inferred or verified geographical location where the video took place")
    tags: List[str] = Field(default_factory=list, description="SEO and classification tags")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    ai_notes: str = Field(..., description="Explanation of why this context and location are accurate, referencing Google Lens clues")
