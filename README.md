# 🎬 YouTube Shorts Generator Agent (LangGraph + Veo 3)

An **AI-powered automation agent** that generates, approves, and uploads YouTube Shorts based on trending topics. Built using **LangGraph**, **Google Veo 3**, **Gemini Pro**, and **YouTube Data API v3**, this tool streamlines your content creation workflow — from idea to upload.

---

## 🚀 Features

- Fetches trending topics (from YouTube)
- Uses Gemini Pro to generate prompt, title & description
- Uses Google Veo 3 to generate an 8-second video
- Human approval using LangGraph interrupts
- Uploads final video directly to YouTube
- Saves topic & URL to a `video_logs.csv` file
- Uses SQLite to checkpoint and resume progress
- Streamlit UI for human approvals and steps

---

## 📁 Project Structure

```bash
│
├── graph.py # LangGraph setup & compilation
├── main.py # Streamlit UI entrypoint
├── state_schema.py # Shared agent state definition
│
├── nodes/
│ ├── topic_selector.py # Trending topic logic
│ ├── prompt_generator.py # Prompt generation using Gemini
│ ├── video_generator.py # Video generation with Veo 3
│ ├── video_uploader.py # YouTube video upload
│ ├── metadata_generator.py # Title/desc generation using Gemini
│ ├── final_logger.py # logging uploaded video data to csv
│
├── checkpoint.sqlite # LangGraph state DB
├── video_logs.csv # Uploaded videos record
├── requirements.txt # Python dependencies
└── README.md # This file
```

---

## 🧠 How It Works
  1. Select Topic → Fetches a trending topic from YouTube
  2. Generate Prompt → Gemini writes a creative script
  3. Generate Video → Veo 3 produces 8-second video
  4. Ask for Approval → You approve or reject topic/video
  5. Generate Metadata → Title and description are created
  6. Upload to YouTube → Video is uploaded to your channel
  7. Log to CSV → Topic and YouTube link are saved

---

## 🛠️ Technologies Used

| 🧩 Technology                 | 📝 Description                                                              |
|-------------------------------|------------------------------------------------------------------------------|
| **LangGraph**                 | Manages agent workflow as a directed graph of nodes                          |
| **Interrupts**                | Pauses execution at key points (topic/video approval) for human feedback     |
| **SQLite Checkpointing**      | Saves agent state between steps using `SqliteSaver`                          |
| **Gemini Pro (Generative AI)**| Generates creative prompts from trending topics using Google's LLM           |
| **Veo 3 (Vertex AI)**         | Generates short videos based on natural language prompts                     |
| **YouTube Data API v3**       | Uploads the final approved video to your YouTube channel                     |


---

## ⚙️ Setup Instructions

#### 1. Clone Repository
```bash
git clone https://github.com/FassihShah/YT-Videos-Agent.git
cd YT-Videos-Agent
```
#### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate 
```
#### 3. Install Requirements
```bash
pip install -r requirements.txt
```
#### 4. Create .env File

 .env file in root directory
```bash
GOOGLE_API_KEY = your_gemini_or_veo_api_key
GOOGLE_CLOUD_PROJECT = your_google_project_id
VEO_BUCKET = your-veo-bucket
```
#### 5. Run the App
```bash
  streamlit run main.py
```

---

## 🔐 How to Setup APIs

### - Veo 3 API Setup (via Vertex AI)

1. Enable Vertex AI API
      - Go to: [Vertex AI API Console](https://console.cloud.google.com/marketplace/product/google/vertex-ai.googleapis.com)
      - Select your GCP project and click Enable
2. Create a Google Cloud Storage (GCS) bucket
      - Set this your .env
3. Set up authentication
      - Use gcloud auth application-default login 
      - Download the JSON key and put in your project folder
4. Set these in your .env:
  ```bash
  GOOGLE_CLOUD_PROJECT=your-gcp-project-id
  VEO_BUCKET=your-gcs-bucket-name
  ```

### - YouTube Data API v3 (Fetch Trending topics and Upload Videos)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select one)
3. Enable these APIs:
     - YouTube Data API v3
     - OAuth 2.0 Client ID
4. Create OAuth credentials:
     - Application type: Desktop App
     - Download the client_secret.json
5. Put it in your project folder
    
🔒 The app will open a browser to authenticate with your Google account and authorize YouTube uploads.

---


