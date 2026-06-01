from groq import Groq
from PIL import Image
import base64
import os
import datetime
import requests
import glob
import io
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def resize_image(image_path):
    img = Image.open(image_path)
    img.thumbnail((5000, 5000))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def ocr_image(image_path):
    image_bytes = resize_image(image_path)
    image_data = base64.b64encode(image_bytes).decode()
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                    {
                        "type": "text",
                        "text": "Transcribe this handwritten diary entry exactly as written.",
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content


def ensure_user():
    r = requests.post(
        "http://localhost:8000/api/v1/auth/register",
        json={
            "user_name": os.getenv("JOURNAL_USER_NAME"),
            "user_age": int(os.getenv("JOURNAL_USER_AGE")),
            "user_password": os.getenv("JOURNAL_USER_PASSWORD"),
            "user_email": os.getenv("JOURNAL_USER_EMAIL"),
        },
    )
    print(f"Register response: {r.status_code} {r.text}")


def ingest(image_path, user_id=1, date=None):
    content = ocr_image(image_path)
    date = date or datetime.date.today().isoformat()
    requests.post(
        "http://localhost:8000/api/v1/journal/create",
        json={"user_id": user_id, "content": content, "date": date},
    )
    print(f"Ingested: {content[:100]}...")


if __name__ == "__main__":
    ensure_user()
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for ext in ["*.jpg", "*.jpeg", "*.png"]:
        for image_path in glob.glob(os.path.join(root, "tests", ext)):
            ingest(image_path)
