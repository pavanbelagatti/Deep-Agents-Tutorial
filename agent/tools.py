"""
agent/tools.py

Search tools for the Competitive Intelligence Deep Agent.
These are plain Python functions — deepagents wraps them as tools automatically.
"""

import os
from typing import Literal
from tavily import TavilyClient

_client: TavilyClient | None = None


def _get_client() -> TavilyClient:
    """Lazily initialize the Tavily client."""
    global _client
    if _client is None:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY is not set. Add it to your .env file.")
        _client = TavilyClient(api_key=api_key)
    return _client


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> dict:
    """
    Search the web for any query.

    Args:
        query: The search query string.
        max_results: How many results to return (default 5).
        topic: "general", "news", or "finance".
        include_raw_content: Include full page text in results.

    Returns:
        Dict with search results — titles, URLs, and snippets.
    """
    return _get_client().search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


def search_news(query: str, max_results: int = 5) -> dict:
    """
    Search for recent news articles about a company or topic.
    Best for: funding rounds, product launches, acquisitions, executive hires.

    Args:
        query: News search query e.g. "Linear funding 2024".
        max_results: How many articles to return.

    Returns:
        Recent news results with titles, URLs, and dates.
    """
    return _get_client().search(query, max_results=max_results, topic="news")


def search_pricing(company_name: str) -> dict:
    """
    Look up a company's current pricing plans and tiers.

    Args:
        company_name: e.g. "Linear", "Notion", "Jira".

    Returns:
        Search results about pricing tiers, free plans, and costs.
    """
    query = f"{company_name} pricing plans tiers 2024 2025"
    return _get_client().search(query, max_results=5)


def search_reviews(company_name: str) -> dict:
    """
    Find customer reviews and ratings for a product.
    Searches G2, Capterra, Reddit, and similar sources.

    Args:
        company_name: Product or company name to research.

    Returns:
        Review summaries, pros/cons, and user sentiment.
    """
    query = f"{company_name} reviews pros cons G2 Capterra Reddit 2024"
    return _get_client().search(query, max_results=5)