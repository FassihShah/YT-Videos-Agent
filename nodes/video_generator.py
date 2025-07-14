from state_schema import AgentState
import time
import os
import subprocess
from google import genai
from dotenv import load_dotenv
from google.genai.types import GenerateVideosConfig
from langgraph.types import interrupt


load_dotenv()


project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
bucket_name = os.getenv("VEO_BUCKET")


def generate_video(prompt: str) -> str:

    # Initialize the GenAI client for Vertex AI
    client = genai.Client(
        vertexai=True,
        project= project_id,
        location="us-central1"
    )

    operation = client.models.generate_videos(
        model="veo-3.0-generate-preview",
        prompt=prompt,
        config=GenerateVideosConfig(
            aspect_ratio="16:9",
            output_gcs_uri=f"gs://{bucket_name}/videos/",
            generate_audio=True
        ),
    )

    print("Waiting for video generation...")
    while not operation.done:
        print("!!still generating...")
        time.sleep(10)
        operation = client.operations.get(operation)

    if operation.response:
        uri = operation.result.generated_videos[0].video.uri
        print("Generated video at:", uri)

        try:
            # Path to gsutil
            GSUTIL_PATH = r"C:\Users\dell\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd"
            os.makedirs("videos", exist_ok=True)

            # Create a timestamp-based filename
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"video_{timestamp}.mp4"
            filepath = os.path.join("videos", filename)

            # Run gsutil command to download
            subprocess.run([GSUTIL_PATH, "cp", uri, filepath], check=True)

            print(f"✅ Downloaded as {filepath}")
            return filepath

        except subprocess.CalledProcessError as e:
            print("Download failed:", e)
            return None

    else:
        print("Generation failed:", operation.error)
        return None
    
    

def video_generator(state: AgentState) -> AgentState:
    prompt = state.get("prompt")
    if not prompt:
        print("No prompt found.")
        return state

    print("Generating video...")
    video_path = generate_video(prompt)
    state["video_path"] = video_path

    return state


def video_approver(state: AgentState) -> AgentState:

    approval = interrupt(f"Do you approve this video?")
    if approval == "yes":
        state["video_approved"] = True
    else:
        state["video_approved"] = False
    return state


def video_decider(state: AgentState) -> str:
    if state.get("video_approved") is True:
        return "metadata_generation"
    else:
        return "video_generation"