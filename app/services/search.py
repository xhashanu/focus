import logging
import os
from typing import Dict, Any, List
from app.config import settings

logger = logging.getLogger(__name__)


class SearchContextService:
    def __init__(self, api_key: str = settings.SERPAPI_API_KEY):
        self.api_key = api_key

    def search_keyframe_context(self, image_path: str) -> Dict[str, Any]:
        """Send keyframe to SerpApi Google Lens to retrieve real-world visual context and location clues."""
        if not self.api_key:
            logger.warning("SERPAPI_API_KEY is not configured. Returning fallback context.")
            return {
                "visual_matches": [],
                "knowledge_graph": {},
                "summary": "No SerpApi key provided. Manual location inspection required.",
                "clues": [],
            }

        try:
            from serpapi import GoogleSearch

            # Google Lens search using SerpApi
            params = {
                "engine": "google_lens",
                "api_key": self.api_key,
            }

            # If image_path is a local file, SerpApi supports direct upload or url
            # For local files, pass url or file parameter based on serpapi version
            if os.path.exists(image_path):
                # Typically passed as file upload or url
                search = GoogleSearch(params)
                # Note: SerpApi client supports file parameter
                with open(image_path, "rb") as f:
                    results = search.get_dict(files={"file": f})
            else:
                params["url"] = image_path
                search = GoogleSearch(params)
                results = search.get_dict()

            visual_matches = results.get("visual_matches", [])
            extracted_clues: List[str] = []
            for match in visual_matches[:5]:
                title = match.get("title")
                source = match.get("source")
                if title:
                    extracted_clues.append(f"{title} ({source})" if source else title)

            return {
                "visual_matches": visual_matches[:5],
                "knowledge_graph": results.get("knowledge_graph", {}),
                "clues": extracted_clues,
                "raw_results": results,
            }
        except Exception as exc:
            logger.error("SerpApi Google Lens search failed for %s: %s", image_path, exc)
            return {
                "visual_matches": [],
                "knowledge_graph": {},
                "summary": f"Context search error: {str(exc)}",
                "clues": [],
                "error": str(exc),
            }


search_service = SearchContextService()
