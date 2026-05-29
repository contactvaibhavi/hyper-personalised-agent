import anthropic, base64, pathlib, requests, datetime

client = anthropic.Anthropic()

for pdf_path in sorted(pathlib.Path("scans/").glob("*.pdf")):
    pdf_data = base64.b64encode(pdf_path.read_bytes()).decode()
    
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "base64",
                 "media_type": "application/pdf", "data": pdf_data}},
                {"type": "text", "text": "Transcribe this handwritten journal page exactly. Preserve paragraph breaks. If a date is visible note it at the top."}
            ]
        }]
    )
    
    requests.post("http://localhost:8000/api/v1/journal/create", json={
        "user_id": 1,
        "content": msg.content[0].text,
        "date": datetime.date.today().isoformat()
    })
    print(f"✓ {pdf_path.name}")