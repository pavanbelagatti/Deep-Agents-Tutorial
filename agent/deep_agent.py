"""
agent/deep_agent.py

Creates and runs the Competitive Intelligence Deep Agent using OpenAI.
"""

import os
import time
from dotenv import load_dotenv
from deepagents import create_deep_agent

from agent.tools import internet_search, search_news, search_pricing, search_reviews
from agent.prompts import COMPETITIVE_INTEL_PROMPT

# Load keys from .env file
load_dotenv()


def build_agent():
    """
    Build and return the deep agent.

    Uses gpt-4o-mini — higher rate limits than gpt-4o, much lower cost.
    Switch to "openai:gpt-4o" only if your account has a paid tier with higher TPM.

    The deep agent automatically gets:
      - write_todos / read_todos  → planning
      - write_file / read_file    → virtual filesystem for large context
      - spawn_subagent            → delegate tasks to child agents
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file.")

    agent = create_deep_agent(
        model="openai:gpt-4o-mini",   # higher rate limits than gpt-4o on free/low tiers
        tools=[
            internet_search,
            search_news,
            search_pricing,
            search_reviews,
        ],
        system_prompt=COMPETITIVE_INTEL_PROMPT,
    )
    return agent


def _extract_text(content) -> str:
    """
    Safely extract a plain string from the agent's last message content.
    The content can be:
      - a plain string  → return as-is
      - a list of blocks like [{"type": "text", "text": "..."}, ...]
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block["text"])
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content)


def run_agent(query: str, max_retries: int = 3) -> str:
    """
    Run the agent on a competitive intelligence query and return the report.
    Automatically retries on 429 rate limit errors with exponential backoff.

    Args:
        query: e.g. "Analyze Notion, Linear, and Asana vs Jira"
        max_retries: how many times to retry on rate limit errors (default 3)

    Returns:
        Final markdown report as a plain string.
    """
    agent = build_agent()

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
            raw_content = result["messages"][-1].content
            return _extract_text(raw_content)

        except Exception as e:
            last_error = e
            err_str = str(e)

            # Check if it's a rate limit error (429)
            if "429" in err_str or "rate_limit_exceeded" in err_str or "Rate limit" in err_str:
                # Extract wait time from error message if available, else use backoff
                wait = 15 * attempt  # 15s, 30s, 45s
                if "Please try again in" in err_str:
                    try:
                        # parse "Please try again in 7.551s"
                        after = err_str.split("Please try again in")[1]
                        seconds_str = after.strip().split("s")[0].strip()
                        wait = int(float(seconds_str)) + 5  # add 5s buffer
                    except Exception:
                        pass

                if attempt < max_retries:
                    # caller (app.py) will show this in the UI via the exception message
                    raise RateLimitError(
                        f"Rate limit hit. Waiting {wait}s before retry "
                        f"(attempt {attempt}/{max_retries})... "
                        f"Consider upgrading your OpenAI plan at "
                        f"https://platform.openai.com/account/rate-limits",
                        wait_seconds=wait,
                        attempt=attempt,
                        max_retries=max_retries,
                    )
            # Non-rate-limit error — re-raise immediately
            raise

    raise last_error


class RateLimitError(Exception):
    """Raised when OpenAI returns a 429. Carries wait time so the UI can show a countdown."""
    def __init__(self, message, wait_seconds, attempt, max_retries):
        super().__init__(message)
        self.wait_seconds = wait_seconds
        self.attempt = attempt
        self.max_retries = max_retries