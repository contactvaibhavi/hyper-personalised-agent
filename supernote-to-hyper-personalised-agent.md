# supernote-to-journalpt

Feed handwritten Supernote Manta diary entries into [hyper-personalised-agent](https://github.com/contactvaibhavi/hyper-personalised-agent) (JournalPT).

## Pipeline

```
Supernote Manta → Export → Text → POST /api/v1/journal/create
```

## Prerequisites

- JournalPT running locally (`python3 app/main.py`)
- Python 3.x + `requests` (`pip install requests`)
- For OCR path: `anthropic` (`pip install anthropic`) + `ANTHROPIC_API_KEY`

---

## Option 1 — Built-in Convert (recommended)

Best quality, no extra tooling.

1. In the Supernote Notes app, tap **Convert** to turn handwriting into text
2. Export as `.txt`
3. Run:

```python
import requests, pathlib, datetime

content = pathlib.Path("entry.txt").read_text()

requests.post("http://localhost:8000/api/v1/journal/create", json={
    "user_id": 1,
    "content": content,
    "date": datetime.date.today().isoformat()
})
```

---

## Option 2 — Image/PDF + Claude OCR

For messy handwriting or when skipping on-device conversion.

1. Export note page as `.png` or `.pdf` via the Supernote app
2. Run:

```python
import anthropic, base64, requests, datetime

client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var
image_data = base64.b64encode(open("note.png", "rb").read()).decode()

msg = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2000,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
            {"type": "text", "text": "Transcribe this handwritten diary entry exactly as written."}
        ]
    }]
)

requests.post("http://localhost:8000/api/v1/journal/create", json={
    "user_id": 1,
    "content": msg.content[0].text,
    "date": datetime.date.today().isoformat()
})
```

---

## Option 3 — Auto-sync via folder watch

Sync Supernote exports to a folder (USB or Supernote Cloud), then watch for new `.txt` files:

```python
import time, pathlib, requests, datetime

WATCH_DIR = pathlib.Path("~/supernote-exports").expanduser()
USER_ID = 1
seen = set()

while True:
    for f in WATCH_DIR.glob("*.txt"):
        if f not in seen:
            requests.post("http://localhost:8000/api/v1/journal/create", json={
                "user_id": USER_ID,
                "content": f.read_text(),
                "date": datetime.date.today().isoformat()
            })
            seen.add(f)
    time.sleep(30)
```

---

## Summarise entries

After ingesting, trigger LLM summarisation:

```bash
curl -XPOST 'http://localhost:8000/api/v1/llm/summarise' \
  --header 'Content-Type: application/json' \
  --data '{"user_id": 1, "days": ["2025-05-29"]}'
```

## Quick comparison

| Method | Quality | Setup effort |
|---|---|---|
| On-device Convert → `.txt` | ★★★★☆ | Low |
| Claude Vision OCR | ★★★★★ | Medium |
| Folder watch automation | ★★★★☆ | Medium |