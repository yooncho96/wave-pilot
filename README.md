# My Kivy App

This repository contains a Kivy-based mobile/desktop application that:

1. Connects to **Google Cloud SQL over SSL**.
2. Uses **OpenAI’s Whisper** to perform speech-to-text.
3. Uses **Azure OpenAI** to detect emotions and store them in the database.

## Features

- **Speech-to-text**: Transcribes an audio file using Whisper.
- **Emotion analysis**: Identifies the severity of 9 emotions (anger, sadness, fear, shame, guilt, jealousy, envy, joy, love) on a scale of 0–10.
- **Database connectivity**: Stores and retrieves transcriptions and emotion scores from a MySQL database hosted on Google Cloud SQL via SSL.
- **Kivy UI**: Provides an interface with multiple screens.

---

## Setup & Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your_username/wave-py-v1.git
   cd wave-py-v1

2. **Create and activate a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate
# On Windows: venv\Scripts\activate

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt

4. **Set up your environment variables or .env file**:
    `OPENAI_API_BASE`, `OPENAI_API_KEY`, `OPENAI_API_VERSION`, `OPENAI_DEPLOYMENT_NAME`
    `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`

5. **Run app**:
    python main.py
