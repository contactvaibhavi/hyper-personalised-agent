# supernote-to-journalpt
Next - summarise and better trancription services

Feed handwritten Supernote Manta diary entries into [hyper-personalised-agent](https://github.com/contactvaibhavi/hyper-personalised-agent) (JournalPT).

## Pipeline

```
Supernote Manta → Export → Text → POST /api/v1/journal/create
```

## Prerequisites

- JournalPT running locally (`python3 app/main.py`)
- Python 3.x + `requests` (`pip install requests`)
- For OCR path: 'groq'

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
