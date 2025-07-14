import csv
from pathlib import Path
from state_schema import AgentState
from datetime import datetime

def final_logger(state: AgentState) -> AgentState:
    """Logs the final video information to a CSV file.
    """
    topic = state.get("topic", "N/A")
    url = state.get("youtube_url", "N/A")
    title = state.get("title", "")
    description = state.get("description", "")
    timestamp = datetime.now().isoformat(timespec="seconds")

    csv_file = Path("video_logs.csv")
    file_exists = csv_file.exists()

    row = {
        "Timestamp": timestamp,
        "Topic": topic,
        "Title": title,
        "Description": description,
        "YouTube URL": url
    }

    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())

        # Write header only if file is new
        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print("Logged video info to CSV.")
    return state
