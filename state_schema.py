from typing import TypedDict, Optional

class AgentState(TypedDict):
    topic: Optional[str]
    topic_approved: Optional[bool]
    prompt: Optional[str]
    video_path: Optional[str]
    video_approved: Optional[bool]
    title: Optional[str]
    description: Optional[str]
    youtube_url: Optional[str]
    upload_success: Optional[bool]
