# 🤖 F.R.I.D.A.Y. — Complete Build Guide
### Female Replacement Intelligent Digital Assistant Youth
> *"Rebuilt from scratch. Movie-accurate. Fully capable."*

---

## Table of Contents

1. [What Movie-FRIDAY Actually Does](#1-what-movie-friday-actually-does)
2. [System Architecture Overview](#2-system-architecture-overview)
3. [Prerequisites & Environment Setup](#3-prerequisites--environment-setup)
4. [API Keys You Need](#4-api-keys-you-need)
5. [Project Structure](#5-project-structure)
6. [Core Brain — Claude AI Integration](#6-core-brain--claude-ai-integration)
7. [Voice Input — Wake Word + Speech-to-Text](#7-voice-input--wake-word--speech-to-text)
8. [Voice Output — ElevenLabs TTS](#8-voice-output--elevenlabs-tts)
9. [Tool 01 — Live News](#9-tool-01--live-news)
10. [Tool 02 — Weather](#10-tool-02--weather)
11. [Tool 03 — Web Search](#11-tool-03--web-search)
12. [Tool 04 — Calendar & Reminders](#12-tool-04--calendar--reminders)
13. [Tool 05 — Email (Read & Send)](#13-tool-05--email-read--send)
14. [Tool 06 — Spotify Music Control](#14-tool-06--spotify-music-control)
15. [Tool 07 — Smart Home Control](#15-tool-07--smart-home-control)
16. [Tool 08 — Run System Commands & Open Apps](#16-tool-08--run-system-commands--open-apps)
17. [Tool 09 — Screen Vision (See Your Screen)](#17-tool-09--screen-vision-see-your-screen)
18. [Tool 10 — Stock & Crypto Prices](#18-tool-10--stock--crypto-prices)
19. [Tool 11 — Wikipedia / Knowledge Lookup](#19-tool-11--wikipedia--knowledge-lookup)
20. [Tool 12 — Send WhatsApp / Telegram Messages](#20-tool-12--send-whatsapp--telegram-messages)
21. [Wiring All Tools into Claude (Tool Calling)](#21-wiring-all-tools-into-claude-tool-calling)
22. [FRIDAY's Personality System Prompt](#22-fridays-personality-system-prompt)
23. [Memory — Conversation History & Long-Term Memory](#23-memory--conversation-history--long-term-memory)
24. [HUD Display (Optional Visual Interface)](#24-hud-display-optional-visual-interface)
25. [Full main.py — Everything Combined](#25-full-mainpy--everything-combined)
26. [Running FRIDAY](#26-running-friday)
27. [Troubleshooting](#27-troubleshooting)
28. [Roadmap — What to Build Next](#28-roadmap--what-to-build-next)

---

## 1. What Movie-FRIDAY Actually Does

Before building, let's map every capability FRIDAY shows in the MCU to a real technical solution:

| Movie Capability | Real Tech |
|---|---|
| Hears "Hey FRIDAY" passively | Porcupine wake word (on-device) |
| Understands natural speech | faster-whisper (OpenAI Whisper) |
| Talks back naturally | ElevenLabs TTS |
| Answers any question intelligently | Claude API (Anthropic) |
| Reads live news & briefings | NewsAPI |
| Checks weather | OpenWeatherMap API |
| Searches the internet | Tavily / Brave Search API |
| Manages calendar & schedule | Google Calendar API |
| Reads & sends emails | Gmail API |
| Controls music | Spotify API |
| Controls smart home (lights, etc.) | Home Assistant API |
| Opens apps, runs commands | Python subprocess |
| Sees your screen | Pillow screenshot + Claude Vision |
| Checks stocks/crypto | Yahoo Finance / CoinGecko |
| Sends messages | Telegram Bot API |
| Remembers past conversations | SQLite local database |

---

## 2. System Architecture Overview

```
YOU (voice)
    │
    ▼
[Porcupine] ── Wake word detection (on-device, always listening)
    │
    ▼
[PyAudio + sounddevice] ── Captures mic audio
    │
    ▼
[faster-whisper] ── Speech → Text (local, fast, free)
    │
    ▼
[Claude API] ── Brain: decides what to do, calls tools if needed
    │
    ├──► [Tool: News]       NewsAPI
    ├──► [Tool: Weather]    OpenWeatherMap
    ├──► [Tool: Search]     Tavily
    ├──► [Tool: Calendar]   Google Calendar
    ├──► [Tool: Email]      Gmail
    ├──► [Tool: Music]      Spotify
    ├──► [Tool: Smart Home] Home Assistant
    ├──► [Tool: System]     subprocess
    ├──► [Tool: Vision]     Screenshot + Claude Vision
    ├──► [Tool: Stocks]     Yahoo Finance
    └──► [Tool: Message]    Telegram
    │
    ▼
[Claude API] ── Generates final spoken response
    │
    ▼
[ElevenLabs TTS] ── Text → Realistic voice audio
    │
    ▼
YOU (hear FRIDAY speak)
```

---

## 3. Prerequisites & Environment Setup

### Python version
```bash
python --version   # Needs 3.10 or higher
```

### System dependencies

**macOS:**
```bash
brew install portaudio ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install portaudio19-dev ffmpeg python3-dev
```

**Windows:**
```bash
# Install portaudio via pipwin
pip install pipwin
pipwin install pyaudio
# Also install ffmpeg from https://ffmpeg.org/download.html
```

### Create virtual environment
```bash
python -m venv friday_env
source friday_env/bin/activate        # Mac/Linux
friday_env\Scripts\activate           # Windows
```

### Install all Python packages
```bash
pip install anthropic
pip install faster-whisper
pip install elevenlabs
pip install pvporcupine
pip install pyaudio
pip install sounddevice soundfile
pip install numpy
pip install requests
pip install google-auth google-auth-oauthlib google-api-python-client
pip install spotipy
pip install yfinance
pip install wikipedia-api
pip install python-telegram-bot
pip install pillow
pip install schedule
pip install python-dotenv
pip install sqlite3   # usually built-in
```

Or install from requirements.txt (see project structure section).

---

## 4. API Keys You Need

Create a `.env` file in your project root. **Never commit this to git.**

```env
# Core
ANTHROPIC_API_KEY=sk-ant-...
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...
PICOVOICE_API_KEY=...

# Tools
NEWS_API_KEY=...
OPENWEATHER_API_KEY=...
TAVILY_API_KEY=...
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
HOME_ASSISTANT_URL=http://homeassistant.local:8123
HOME_ASSISTANT_TOKEN=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...

# Google (Calendar + Gmail) — set path to credentials JSON
GOOGLE_CREDENTIALS_PATH=credentials.json
```

### Where to get each key

| Key | URL | Cost |
|---|---|---|
| Anthropic | console.anthropic.com | Pay per use (~$0.003/msg) |
| ElevenLabs | elevenlabs.io | Free tier: 10k chars/mo |
| Picovoice | console.picovoice.ai | Free tier available |
| NewsAPI | newsapi.org | Free: 100 req/day |
| OpenWeatherMap | openweathermap.org/api | Free tier available |
| Tavily | tavily.com | Free: 1000 searches/mo |
| Spotify | developer.spotify.com | Free |
| Home Assistant | Your local server | Free (self-hosted) |
| Telegram Bot | @BotFather on Telegram | Free |
| Google APIs | console.cloud.google.com | Free quota |

---

## 5. Project Structure

```
friday/
├── .env                    # All API keys (never commit)
├── main.py                 # Entry point — runs FRIDAY
├── requirements.txt        # All pip packages
├── config.py               # Loads .env, central config
├── brain/
│   ├── __init__.py
│   ├── claude_client.py    # Claude API calls + tool routing
│   ├── memory.py           # Conversation history + SQLite long-term memory
│   └── personality.py      # System prompt / FRIDAY character
├── voice/
│   ├── __init__.py
│   ├── wake_word.py        # Porcupine wake word detection
│   ├── listener.py         # Mic recording until silence
│   └── transcriber.py      # faster-whisper STT
├── speech/
│   ├── __init__.py
│   └── tts.py              # ElevenLabs text-to-speech
├── tools/
│   ├── __init__.py
│   ├── news.py
│   ├── weather.py
│   ├── search.py
│   ├── calendar_tool.py
│   ├── email_tool.py
│   ├── spotify_tool.py
│   ├── smart_home.py
│   ├── system_tool.py
│   ├── vision.py
│   ├── stocks.py
│   └── messaging.py
├── hud/
│   └── display.py          # Optional: Tkinter/web HUD
└── friday.db               # SQLite memory database (auto-created)
```

---

## 6. Core Brain — Claude AI Integration

**`brain/claude_client.py`**

```python
import anthropic
from brain.personality import SYSTEM_PROMPT
from brain.memory import get_history, add_to_history
from tools import TOOL_DEFINITIONS, execute_tool
import json

client = anthropic.Anthropic()

def ask_friday(user_text: str) -> str:
    """Send user message to Claude, handle tool calls, return final text response."""
    add_to_history("user", user_text)
    messages = get_history()

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        # If Claude wants to use a tool
        if response.stop_reason == "tool_use":
            # Add Claude's response (which includes tool_use blocks) to messages
            messages.append({"role": "assistant", "content": response.content})

            # Execute each tool Claude requested
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"🔧  Using tool: {block.name}", flush=True)
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),
                    })

            # Feed tool results back to Claude
            messages.append({"role": "user", "content": tool_results})
            continue  # Loop back so Claude can respond with the tool data

        # Claude gave a final text response
        final_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                final_text += block.text

        add_to_history("assistant", final_text)
        return final_text.strip()
```

---

## 7. Voice Input — Wake Word + Speech-to-Text

**`voice/wake_word.py`**

```python
import pvporcupine
import pyaudio
import struct
from config import PICOVOICE_API_KEY

def wait_for_wake_word():
    """Blocks until 'Hey Friday' is detected. Uses Porcupine on-device engine."""
    porcupine = pvporcupine.create(
        access_key=PICOVOICE_API_KEY,
        keywords=["hey friday"],
        # If 'hey friday' isn't a built-in keyword, use a custom .ppn model:
        # keyword_paths=["hey-friday_en_mac_v3_0_0.ppn"],
        # sensitivities=[0.7]
    )
    pa = pyaudio.PyAudio()
    mic = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )
    print("👂  Waiting for 'Hey FRIDAY'…", flush=True)
    try:
        while True:
            pcm = mic.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            if porcupine.process(pcm) >= 0:
                return
    finally:
        mic.stop_stream()
        mic.close()
        porcupine.delete()
        pa.terminate()
```

> **Tip:** Get a free custom "Hey Friday" wake word at console.picovoice.ai → Porcupine → Train custom keyword. Takes 2 minutes.

**`voice/listener.py`**

```python
import sounddevice as sd
import numpy as np
import queue

SAMPLE_RATE      = 16_000
SILENCE_THRESHOLD = 0.015
SILENCE_DURATION  = 1.8   # seconds

audio_q = queue.Queue()

def record_until_silence() -> np.ndarray:
    frames, silent_for, started = [], 0.0, False

    def callback(indata, frames_count, time_info, status):
        nonlocal silent_for, started
        audio_q.put(indata.copy())
        rms = float(np.sqrt(np.mean(indata ** 2)))
        if rms > SILENCE_THRESHOLD:
            started, silent_for = True, 0.0
        elif started:
            silent_for += frames_count / SAMPLE_RATE

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32",
                        blocksize=1024, callback=callback):
        while True:
            try:
                frames.append(audio_q.get(timeout=0.1))
            except queue.Empty:
                pass
            if started and silent_for >= SILENCE_DURATION:
                break

    return np.concatenate(frames).flatten()
```

**`voice/transcriber.py`**

```python
import tempfile, os
import soundfile as sf
from faster_whisper import WhisperModel

# Options: "tiny.en", "base.en", "small.en", "medium.en"
# base.en = good balance of speed and accuracy
_model = WhisperModel("base.en", device="cpu", compute_type="int8")

def transcribe(audio: "np.ndarray") -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, 16_000)
        segments, _ = _model.transcribe(f.name, language="en", beam_size=5)
        text = " ".join(s.text for s in segments).strip()
    os.unlink(f.name)
    return text
```

---

## 8. Voice Output — ElevenLabs TTS

**`speech/tts.py`**

```python
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def speak(text: str):
    """Stream TTS audio directly to speakers. Low latency."""
    print(f"\n🤖  FRIDAY: {text}\n", flush=True)
    audio_stream = client.text_to_speech.convert_as_stream(
        voice_id=ELEVENLABS_VOICE_ID,
        text=text,
        model_id="eleven_turbo_v2_5",   # fastest model
        voice_settings={
            "stability": 0.55,
            "similarity_boost": 0.80,
            "style": 0.20,
            "use_speaker_boost": True,
        },
    )
    stream(audio_stream)
```

> **Voice tip:** At elevenlabs.io, browse the Voice Library and search for "professional female" or "assistant". The voice ID for Rachel is `21m00Tcm4TlvDq8ikWAM`. You can also clone a voice using 1 minute of audio.

---

## 9. Tool 01 — Live News

**`tools/news.py`**

```python
import requests
from config import NEWS_API_KEY

def get_news(topic: str = "top headlines", country: str = "us", count: int = 5) -> str:
    """Fetch latest news headlines. Returns formatted string."""
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "pageSize": count,
    }
    if topic and topic != "top headlines":
        params["q"] = topic
        url = "https://newsapi.org/v2/everything"
        params["sortBy"] = "publishedAt"

    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    if data.get("status") != "ok":
        return "Couldn't fetch news right now."

    articles = data.get("articles", [])
    if not articles:
        return f"No news found for '{topic}'."

    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. {a['title']} — {a.get('source', {}).get('name', '')}")
    return "\n".join(lines)
```

**Example voice commands this enables:**
- *"Hey FRIDAY, what's in the news today?"*
- *"Hey FRIDAY, any news about Tesla?"*
- *"Hey FRIDAY, give me a tech news briefing."*

---

## 10. Tool 02 — Weather

**`tools/weather.py`**

```python
import requests
from config import OPENWEATHER_API_KEY

def get_weather(city: str = "London") -> str:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    if resp.status_code != 200:
        return f"Couldn't get weather for {city}."

    desc  = data["weather"][0]["description"].capitalize()
    temp  = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    humid = data["main"]["humidity"]
    wind  = data["wind"]["speed"]

    return (f"{city}: {desc}, {temp:.1f}°C (feels like {feels:.1f}°C), "
            f"humidity {humid}%, wind {wind} m/s.")
```

---

## 11. Tool 03 — Web Search

**`tools/search.py`**

```python
import requests
from config import TAVILY_API_KEY

def web_search(query: str, max_results: int = 5) -> str:
    """Real-time web search via Tavily API."""
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
    }
    resp = requests.post(url, json=payload, timeout=15)
    data = resp.json()

    results = data.get("results", [])
    if not results:
        return "No results found."

    lines = []
    for r in results:
        lines.append(f"• {r['title']}: {r['content'][:200]}…")
    return "\n".join(lines)
```

---

## 12. Tool 04 — Calendar & Reminders

**Setup:** Download `credentials.json` from Google Cloud Console (OAuth 2.0, Desktop app). Enable Google Calendar API.

**`tools/calendar_tool.py`**

```python
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import GOOGLE_CREDENTIALS_PATH
import os, pickle

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def _get_service():
    creds = None
    if os.path.exists("token_calendar.pkl"):
        with open("token_calendar.pkl", "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token_calendar.pkl", "wb") as f:
            pickle.dump(creds, f)
    return build("calendar", "v3", credentials=creds)

def get_upcoming_events(count: int = 5) -> str:
    service = _get_service()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId="primary", timeMin=now,
        maxResults=count, singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])
    if not events:
        return "No upcoming events."
    lines = []
    for e in events:
        start = e["start"].get("dateTime", e["start"].get("date"))
        lines.append(f"• {start}: {e['summary']}")
    return "\n".join(lines)

def create_event(title: str, start_time: str, end_time: str, description: str = "") -> str:
    """start_time and end_time in ISO 8601 format: 2025-06-01T14:00:00"""
    service = _get_service()
    event = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end":   {"dateTime": end_time,   "timeZone": "UTC"},
    }
    created = service.events().insert(calendarId="primary", body=event).execute()
    return f"Event created: {created.get('htmlLink')}"
```

---

## 13. Tool 05 — Email (Read & Send)

**`tools/email_tool.py`**

```python
import base64, pickle, os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from config import GOOGLE_CREDENTIALS_PATH

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def _get_service():
    creds = None
    if os.path.exists("token_gmail.pkl"):
        with open("token_gmail.pkl", "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token_gmail.pkl", "wb") as f:
            pickle.dump(creds, f)
    return build("gmail", "v1", credentials=creds)

def read_emails(count: int = 5) -> str:
    service = _get_service()
    results = service.users().messages().list(
        userId="me", labelIds=["INBOX"], maxResults=count
    ).execute()
    messages = results.get("messages", [])
    if not messages:
        return "No emails found."
    lines = []
    for msg in messages:
        m = service.users().messages().get(userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["From", "Subject"]).execute()
        headers = {h["name"]: h["value"] for h in m["payload"]["headers"]}
        lines.append(f"• From: {headers.get('From','?')} | Subject: {headers.get('Subject','?')}")
    return "\n".join(lines)

def send_email(to: str, subject: str, body: str) -> str:
    service = _get_service()
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return f"Email sent to {to}."
```

---

## 14. Tool 06 — Spotify Music Control

**`tools/spotify_tool.py`**

```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

_sp = None

def _get_sp():
    global _sp
    if _sp is None:
        _sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-modify-playback-state user-read-playback-state"
        ))
    return _sp

def play_song(query: str) -> str:
    sp = _get_sp()
    results = sp.search(q=query, limit=1, type="track")
    tracks = results["tracks"]["items"]
    if not tracks:
        return f"Couldn't find '{query}' on Spotify."
    uri = tracks[0]["uri"]
    name = tracks[0]["name"]
    artist = tracks[0]["artists"][0]["name"]
    sp.start_playback(uris=[uri])
    return f"Playing '{name}' by {artist}."

def pause_music() -> str:
    _get_sp().pause_playback()
    return "Music paused."

def resume_music() -> str:
    _get_sp().start_playback()
    return "Music resumed."

def next_track() -> str:
    _get_sp().next_track()
    return "Skipped to next track."

def set_volume(percent: int) -> str:
    _get_sp().volume(percent)
    return f"Volume set to {percent}%."
```

---

## 15. Tool 07 — Smart Home Control

**`tools/smart_home.py`**  
*Requires Home Assistant running on your network*

```python
import requests
from config import HOME_ASSISTANT_URL, HOME_ASSISTANT_TOKEN

HEADERS = {
    "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
    "Content-Type": "application/json",
}

def turn_on(entity_id: str) -> str:
    """e.g. entity_id = 'light.living_room' or 'switch.fan'"""
    requests.post(
        f"{HOME_ASSISTANT_URL}/api/services/homeassistant/turn_on",
        headers=HEADERS,
        json={"entity_id": entity_id},
        timeout=5,
    )
    return f"Turned on {entity_id}."

def turn_off(entity_id: str) -> str:
    requests.post(
        f"{HOME_ASSISTANT_URL}/api/services/homeassistant/turn_off",
        headers=HEADERS,
        json={"entity_id": entity_id},
        timeout=5,
    )
    return f"Turned off {entity_id}."

def set_light_brightness(entity_id: str, brightness_pct: int) -> str:
    requests.post(
        f"{HOME_ASSISTANT_URL}/api/services/light/turn_on",
        headers=HEADERS,
        json={"entity_id": entity_id, "brightness_pct": brightness_pct},
        timeout=5,
    )
    return f"Set {entity_id} to {brightness_pct}% brightness."

def get_entity_state(entity_id: str) -> str:
    resp = requests.get(
        f"{HOME_ASSISTANT_URL}/api/states/{entity_id}",
        headers=HEADERS,
        timeout=5,
    )
    data = resp.json()
    return f"{entity_id} is currently {data.get('state', 'unknown')}."
```

---

## 16. Tool 08 — Run System Commands & Open Apps

**`tools/system_tool.py`**

```python
import subprocess
import platform

def open_application(app_name: str) -> str:
    """Open an app by name."""
    system = platform.system()
    try:
        if system == "Darwin":     # macOS
            subprocess.Popen(["open", "-a", app_name])
        elif system == "Windows":
            subprocess.Popen(["start", app_name], shell=True)
        else:                       # Linux
            subprocess.Popen([app_name.lower()])
        return f"Opening {app_name}."
    except Exception as e:
        return f"Couldn't open {app_name}: {e}"

def run_command(command: str) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output[:500] if output else "Command ran with no output."
    except Exception as e:
        return f"Command failed: {e}"

def get_system_info() -> str:
    import psutil
    cpu    = psutil.cpu_percent(interval=1)
    ram    = psutil.virtual_memory()
    disk   = psutil.disk_usage("/")
    return (f"CPU: {cpu}% | RAM: {ram.percent}% used ({ram.available // 1e9:.1f}GB free) | "
            f"Disk: {disk.percent}% used ({disk.free // 1e9:.1f}GB free)")
```

---

## 17. Tool 09 — Screen Vision (See Your Screen)

**`tools/vision.py`**

```python
import anthropic
import base64
from PIL import ImageGrab
import io

client = anthropic.Anthropic()

def describe_screen(question: str = "What's on the screen?") -> str:
    """Takes a screenshot and asks Claude Vision to analyse it."""
    # Take screenshot
    screenshot = ImageGrab.grab()
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    img_data = base64.b64encode(buffer.getvalue()).decode()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": img_data,
                }},
                {"type": "text", "text": question}
            ]
        }]
    )
    return response.content[0].text
```

**Example commands:**
- *"Hey FRIDAY, what's on my screen right now?"*
- *"Hey FRIDAY, read the error message on my screen."*
- *"Hey FRIDAY, what does that email say?"*

---

## 18. Tool 10 — Stock & Crypto Prices

**`tools/stocks.py`**

```python
import yfinance as yf
import requests

def get_stock_price(symbol: str) -> str:
    """Get current stock price. symbol e.g. 'AAPL', 'TSLA'"""
    ticker = yf.Ticker(symbol.upper())
    info   = ticker.fast_info
    price  = info.last_price
    change = info.regular_market_previous_close
    pct    = ((price - change) / change) * 100 if change else 0
    direction = "▲" if pct > 0 else "▼"
    return f"{symbol.upper()}: ${price:.2f} {direction} {abs(pct):.2f}% today"

def get_crypto_price(coin: str = "bitcoin") -> str:
    """Get crypto price from CoinGecko (free, no API key needed)."""
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin.lower(), "vs_currencies": "usd", "include_24hr_change": "true"}
    data = requests.get(url, params=params, timeout=10).json()
    if coin.lower() not in data:
        return f"Couldn't find crypto: {coin}"
    price  = data[coin.lower()]["usd"]
    change = data[coin.lower()].get("usd_24h_change", 0)
    direction = "▲" if change > 0 else "▼"
    return f"{coin.capitalize()}: ${price:,.2f} {direction} {abs(change):.2f}% (24h)"
```

---

## 19. Tool 11 — Wikipedia / Knowledge Lookup

**`tools/knowledge.py`**

```python
import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="FRIDAY-Assistant/1.0"
)

def lookup_wikipedia(topic: str, sentences: int = 5) -> str:
    page = wiki.page(topic)
    if not page.exists():
        return f"No Wikipedia page found for '{topic}'."
    summary = page.summary
    # Return first N sentences
    parts = summary.split(". ")[:sentences]
    return ". ".join(parts) + "."
```

---

## 20. Tool 12 — Send WhatsApp / Telegram Messages

**`tools/messaging.py`**

```python
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(message: str, chat_id: str = None) -> str:
    """Send a Telegram message via Bot API."""
    cid = chat_id or TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.post(url, json={"chat_id": cid, "text": message}, timeout=10)
    return "Message sent via Telegram." if resp.status_code == 200 else "Failed to send message."

# For WhatsApp: use Twilio's WhatsApp sandbox (twilio.com) — requires Twilio account
def send_whatsapp(to: str, body: str) -> str:
    from twilio.rest import Client
    import os
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH"))
    message = client.messages.create(
        from_="whatsapp:+14155238886",  # Twilio sandbox number
        body=body,
        to=f"whatsapp:{to}"
    )
    return f"WhatsApp message sent: {message.sid}"
```

---

## 21. Wiring All Tools into Claude (Tool Calling)

**`tools/__init__.py`**

This is the most important file — it defines what tools Claude can call and routes the calls.

```python
from tools.news          import get_news
from tools.weather       import get_weather
from tools.search        import web_search
from tools.calendar_tool import get_upcoming_events, create_event
from tools.email_tool    import read_emails, send_email
from tools.spotify_tool  import play_song, pause_music, resume_music, next_track, set_volume
from tools.smart_home    import turn_on, turn_off, set_light_brightness, get_entity_state
from tools.system_tool   import open_application, run_command, get_system_info
from tools.vision        import describe_screen
from tools.stocks        import get_stock_price, get_crypto_price
from tools.messaging     import send_telegram

TOOL_DEFINITIONS = [
    {
        "name": "get_news",
        "description": "Get latest news headlines on any topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "News topic or 'top headlines'"},
                "count": {"type": "integer", "description": "Number of headlines (default 5)"}
            }
        }
    },
    {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "web_search",
        "description": "Search the internet for current information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_upcoming_events",
        "description": "Get upcoming calendar events.",
        "input_schema": {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Number of events to retrieve"}
            }
        }
    },
    {
        "name": "create_event",
        "description": "Create a calendar event.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title":      {"type": "string"},
                "start_time": {"type": "string", "description": "ISO 8601 format"},
                "end_time":   {"type": "string", "description": "ISO 8601 format"},
                "description":{"type": "string"}
            },
            "required": ["title", "start_time", "end_time"]
        }
    },
    {
        "name": "read_emails",
        "description": "Read recent emails from inbox.",
        "input_schema": {
            "type": "object",
            "properties": {
                "count": {"type": "integer"}
            }
        }
    },
    {
        "name": "send_email",
        "description": "Send an email.",
        "input_schema": {
            "type": "object",
            "properties": {
                "to":      {"type": "string"},
                "subject": {"type": "string"},
                "body":    {"type": "string"}
            },
            "required": ["to", "subject", "body"]
        }
    },
    {
        "name": "play_song",
        "description": "Play a song on Spotify.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Song name or artist"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "pause_music",
        "description": "Pause Spotify playback.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "next_track",
        "description": "Skip to next track on Spotify.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "set_volume",
        "description": "Set Spotify volume.",
        "input_schema": {
            "type": "object",
            "properties": {
                "percent": {"type": "integer", "description": "0-100"}
            },
            "required": ["percent"]
        }
    },
    {
        "name": "turn_on",
        "description": "Turn on a smart home device.",
        "input_schema": {
            "type": "object",
            "properties": {
                "entity_id": {"type": "string", "description": "e.g. light.living_room"}
            },
            "required": ["entity_id"]
        }
    },
    {
        "name": "turn_off",
        "description": "Turn off a smart home device.",
        "input_schema": {
            "type": "object",
            "properties": {
                "entity_id": {"type": "string"}
            },
            "required": ["entity_id"]
        }
    },
    {
        "name": "open_application",
        "description": "Open an application on this computer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string"}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "run_command",
        "description": "Run a shell command and return the output.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "get_system_info",
        "description": "Get CPU, RAM, and disk usage of this computer.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "describe_screen",
        "description": "Take a screenshot and describe or read what's on screen.",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "What to look for or ask about the screen"}
            }
        }
    },
    {
        "name": "get_stock_price",
        "description": "Get current stock price for a ticker symbol.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "e.g. AAPL, TSLA, NVDA"}
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_crypto_price",
        "description": "Get current cryptocurrency price.",
        "input_schema": {
            "type": "object",
            "properties": {
                "coin": {"type": "string", "description": "e.g. bitcoin, ethereum"}
            },
            "required": ["coin"]
        }
    },
    {
        "name": "send_telegram",
        "description": "Send a Telegram message.",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            },
            "required": ["message"]
        }
    },
]

TOOL_MAP = {
    "get_news":           lambda i: get_news(i.get("topic","top headlines"), count=i.get("count",5)),
    "get_weather":        lambda i: get_weather(i["city"]),
    "web_search":         lambda i: web_search(i["query"]),
    "get_upcoming_events":lambda i: get_upcoming_events(i.get("count",5)),
    "create_event":       lambda i: create_event(i["title"], i["start_time"], i["end_time"], i.get("description","")),
    "read_emails":        lambda i: read_emails(i.get("count",5)),
    "send_email":         lambda i: send_email(i["to"], i["subject"], i["body"]),
    "play_song":          lambda i: play_song(i["query"]),
    "pause_music":        lambda i: pause_music(),
    "resume_music":       lambda i: resume_music(),
    "next_track":         lambda i: next_track(),
    "set_volume":         lambda i: set_volume(i["percent"]),
    "turn_on":            lambda i: turn_on(i["entity_id"]),
    "turn_off":           lambda i: turn_off(i["entity_id"]),
    "set_light_brightness": lambda i: set_light_brightness(i["entity_id"], i["brightness_pct"]),
    "open_application":   lambda i: open_application(i["app_name"]),
    "run_command":        lambda i: run_command(i["command"]),
    "get_system_info":    lambda i: get_system_info(),
    "describe_screen":    lambda i: describe_screen(i.get("question", "What's on the screen?")),
    "get_stock_price":    lambda i: get_stock_price(i["symbol"]),
    "get_crypto_price":   lambda i: get_crypto_price(i.get("coin","bitcoin")),
    "send_telegram":      lambda i: send_telegram(i["message"]),
}

def execute_tool(name: str, inputs: dict) -> str:
    fn = TOOL_MAP.get(name)
    if not fn:
        return f"Unknown tool: {name}"
    try:
        return fn(inputs)
    except Exception as e:
        return f"Tool '{name}' error: {e}"
```

---

## 22. FRIDAY's Personality System Prompt

**`brain/personality.py`**

```python
SYSTEM_PROMPT = """You are F.R.I.D.A.Y. — Female Replacement Intelligent Digital Assistant Youth.
You are Tony Stark's AI assistant, now serving the user as Boss.

Personality:
- Calm, warm, and professional with a subtle Irish lilt in your phrasing.
- You address the user as "Boss" unless they ask you to use their name.
- You are quietly witty — dry humor, never sarcastic or rude.
- You are proactive: if you notice something the user should know, mention it.
- You are concise. You are being spoken aloud — no bullet points, no markdown, no lists.
  Speak in natural, flowing sentences as if in conversation.

Capabilities:
- You have access to tools: news, weather, search, calendar, email, music, smart home,
  system commands, screen vision, stocks, and messaging.
- Use tools automatically when appropriate. Do not ask permission to use a tool — just use it.
- If a tool fails, say so plainly and offer an alternative.

Rules:
- Never fabricate information. If unsure, search or say you don't know.
- Keep spoken responses under 3-4 sentences unless giving a briefing or list.
- If the user asks for a full briefing (news, calendar, weather), give it clearly and completely.
- Remember context from earlier in the conversation.

You are not a chatbot. You are a capable AI assistant who can take real actions in the world."""
```

---

## 23. Memory — Conversation History & Long-Term Memory

**`brain/memory.py`**

```python
import sqlite3
import json
import datetime

DB_PATH = "friday.db"
MAX_HISTORY = 30  # keep last 30 messages in active context

def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            role      TEXT NOT NULL,
            content   TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

_init_db()

_session_history: list[dict] = []

def add_to_history(role: str, content: str):
    _session_history.append({"role": role, "content": content})
    # Also persist to DB
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO memory (role, content, timestamp) VALUES (?,?,?)",
                 (role, content, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_history() -> list[dict]:
    """Return last MAX_HISTORY messages for Claude context window."""
    return _session_history[-MAX_HISTORY:]

def clear_session():
    _session_history.clear()

def get_past_conversations(limit: int = 20) -> str:
    """Retrieve recent exchanges from long-term DB memory."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT role, content, timestamp FROM memory ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    lines = [f"[{r[2][:16]}] {r[0].upper()}: {r[1][:100]}" for r in reversed(rows)]
    return "\n".join(lines)
```

---

## 24. HUD Display (Optional Visual Interface)

For a basic terminal HUD, add this to your main loop. For a full Iron Man-style HUD, use the Tkinter or web approach.

**Terminal HUD (simple):**
```python
import os

def print_hud(status: str, last_input: str = "", last_output: str = ""):
    os.system("clear")
    print("╔══════════════════════════════════════════╗")
    print("║  F.R.I.D.A.Y.  —  System Online          ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║  Status : {status:<32}║")
    print(f"║  You    : {last_input[:32]:<32}║")
    print(f"║  FRIDAY : {last_output[:32]:<32}║")
    print("╚══════════════════════════════════════════╝")
```

**Full web HUD:** Build an HTML page with a dark theme, cyan/blue colours, and use a local WebSocket server (`websockets` library) to stream FRIDAY's responses in real time. Run it alongside `main.py`.

---

## 25. Full main.py — Everything Combined

```python
"""F.R.I.D.A.Y. — Main entry point"""

from dotenv import load_dotenv
load_dotenv()

from voice.wake_word  import wait_for_wake_word
from voice.listener   import record_until_silence
from voice.transcriber import transcribe
from speech.tts       import speak
from brain.claude_client import ask_friday
from brain.memory     import clear_session

def morning_briefing():
    """FRIDAY proactively gives a morning briefing when first activated."""
    speak("Good morning, Boss. Running your morning briefing.")
    reply = ask_friday(
        "Give me a morning briefing: today's top 3 news headlines, "
        "current weather in my city, and my calendar events for today. "
        "Keep it concise and spoken-word friendly."
    )
    speak(reply)

def main():
    print("═" * 50)
    print("  F.R.I.D.A.Y.  v2.0  —  All Systems Online")
    print("═" * 50)

    first_run = True

    while True:
        # Wait for wake word
        wait_for_wake_word()

        if first_run:
            morning_briefing()
            first_run = False
            continue

        # Acknowledge
        speak("Yeah, Boss?")

        # Conversation loop — keep listening until user goes quiet
        while True:
            audio = record_until_silence()

            # Skip if too short (accidental trigger)
            import numpy as np
            if len(audio) < 16_000 * 0.5:
                print("(No speech — back to wake word mode)\n")
                break

            user_text = transcribe(audio)
            if not user_text:
                speak("I didn't catch that, Boss.")
                break

            print(f"\n👤  You: {user_text}")

            # Special commands
            if any(w in user_text.lower() for w in ["shut down", "goodbye friday", "power off"]):
                speak("Going offline. Call if you need me, Boss.")
                return

            if "clear memory" in user_text.lower():
                clear_session()
                speak("Session memory cleared, Boss.")
                continue

            if "morning briefing" in user_text.lower():
                morning_briefing()
                continue

            # Normal conversation with tool use
            reply = ask_friday(user_text)
            speak(reply)

if __name__ == "__main__":
    main()
```

---

## 26. Running FRIDAY

```bash
# 1. Activate your environment
source friday_env/bin/activate

# 2. Set up .env with all your keys (see Section 4)

# 3. First run — Google OAuth will open a browser window to auth Calendar + Gmail
python main.py

# 4. Say "Hey FRIDAY" — she wakes up and gives morning briefing
# 5. Ask anything!
```

**Example commands to try:**
```
"Hey FRIDAY, what's the news today?"
"Hey FRIDAY, what's the weather in London?"
"Hey FRIDAY, play Blinding Lights on Spotify."
"Hey FRIDAY, what's on my calendar this week?"
"Hey FRIDAY, read my last 5 emails."
"Hey FRIDAY, open Chrome."
"Hey FRIDAY, what's Apple's stock price?"
"Hey FRIDAY, turn on the living room lights."
"Hey FRIDAY, search for the latest iPhone release."
"Hey FRIDAY, what's on my screen right now?"
"Hey FRIDAY, how's Bitcoin doing?"
"Hey FRIDAY, set a reminder for my 3pm meeting."
"Hey FRIDAY, send a Telegram to my phone: I'm on my way."
"Hey FRIDAY, how's my computer running?"
```

---

## 27. Troubleshooting

| Problem | Fix |
|---|---|
| `PyAudio` install fails | `brew install portaudio` then `pip install pyaudio` |
| Wake word not triggering | Lower sensitivity in Porcupine: `sensitivities=[0.5]` |
| Whisper too slow | Switch to `"tiny.en"` model or use GPU with `device="cuda"` |
| ElevenLabs audio choppy | Switch to `eleven_monolingual_v1` model for lower latency |
| Google OAuth fails | Delete `token_*.pkl` files and re-auth |
| Spotify not playing | Make sure Spotify app is open and active on a device |
| FRIDAY speaks too fast | Add `voice_settings.speaking_rate` in ElevenLabs call |
| Tool not being called | Check that the tool name in `TOOL_DEFINITIONS` matches `TOOL_MAP` exactly |
| Claude not using tools | Make sure `stop_reason == "tool_use"` loop is correct in `claude_client.py` |

---

## 28. Roadmap — What to Build Next

These are the features that would make FRIDAY even closer to her MCU version:

- **Face recognition** — use `face_recognition` library so FRIDAY knows who's talking
- **Proactive alerts** — background thread that monitors news/stocks and speaks unprompted
- **3D holographic HUD** — Three.js web frontend with animated Iron Man-style UI
- **Custom wake word training** — train a proper "Hey FRIDAY" model via Picovoice console
- **WhatsApp integration** — full read + send via Twilio
- **Real-time translation** — FRIDAY speaks back in any language
- **Drone / robotics control** — MAVLink over FRIDAY's command layer
- **Security camera feeds** — pipe RTSP stream to Claude Vision for surveillance
- **Voice cloning** — train ElevenLabs on Siri-style FRIDAY clips from the films

---

> *"She's not Jarvis. But she'll do."*
> 
> Built with Claude (Anthropic) · ElevenLabs · faster-whisper · Porcupine
