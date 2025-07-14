import os
from typing import Optional
from state_schema import AgentState
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# OAuth Constants
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = "client_secrets.json"
CREDENTIALS_FILE = "token.json"


def get_youtube_service():
    """
    Authenticates and returns a YouTube service object.
    """
    creds: Optional[Credentials] = None

    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=8080)
        with open(CREDENTIALS_FILE, "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def upload_video_to_youtube(file_path: str, title: str, description: str) -> str:
    """Uploads the video and returns the YouTube video URL.
    """
    youtube = get_youtube_service()

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(file_path, mimetype="video/*", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    print("Uploading video to YouTube...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    video_url = f"https://youtube.com/watch?v={response['id']}"
    print("Upload completed:", video_url)
    return video_url


# LangGraph node for uploading video to YouTube
def video_uploader(state: AgentState) -> AgentState:
    """
        Uploads a video to YouTube using the provided state information.
    """
    try:
        file_path = state.get("video_path")
        title = state.get("title")
        description = state.get("description")

        if not all([file_path, title, description]):
            raise ValueError("Missing file_path, title, or description in state.")

        video_url = upload_video_to_youtube(file_path, title, description)

        state["youtube_url"] = video_url
        state["upload_success"] = True

        return state

    except Exception as e:
        print("Upload failed:", e)

        state["upload_success"] = False
        return state
