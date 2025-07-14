import os
import requests
import random
from dotenv import load_dotenv
from langgraph.types import interrupt
from state_schema import AgentState


load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def topic_decider(state: AgentState) -> str:
    if state.get("topic_approved") is True:
        return "prompt_generation"
    else:
        return "topic_selection"
    

def fetch_trending_titles(region_code: str = "PK", max_results: int = 10) -> list[str]:
    """
    Fetches trending video titles using the YouTube Data API v3.
    """
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    titles = [item["snippet"]["title"] for item in data.get("items", [])]

    return titles


def pick_topic_from_titles(titles: list[str]) -> str:
    """
    Picks a trending topic from video titles. 
    Currently random, but you can add NLP logic later.
    """
    if not titles:
        return "Satisfying Rock Breaking"

    return random.choice(titles)



# LangGraph node function
# This function will be used in the LangGraph workflow to select a topic
def topic_selector(state: AgentState) -> AgentState:
    """ Selects a topic from trending YouTube video titles.
    """
    try:
        titles = fetch_trending_titles()
        topic = pick_topic_from_titles(titles)

        if not topic:
            raise ValueError("Failed to select a topic.")

        print(f"Selected topic: {topic}")
        state["topic"] = topic
        return state

    except Exception as e:
        print(f"[topic_selector] Error: {e}")
        fallback = "Satisfying Rock Breaking"
        state["topic"] = fallback
        return state
    

def topic_approver(state: AgentState) -> AgentState:

    topic = state["topic"]
    
    approval = interrupt(f"Do you approve this topic? {topic}")

    if approval == "yes":
        state["topic_approved"] = True
    else:
        state["topic_approved"] = False
    return state







