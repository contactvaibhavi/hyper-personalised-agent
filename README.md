# Hyper-personalised Agent

### 06 - [Journals ingestion](./docs/supernote-to-hyper-personalised-agent.md)
### 06 - [Pattern-Trigger](./docs/pattern-trigger.md)

## Installation

### macOS

- Setup python environment:

```bash
python3 -m venv env
source env/bin/activate
pip3 install --upgrade pip

pip3 install psycopg2-binary
pip3 install -r requirements.txt
```

- Install [Postgresql](https://postgresapp.com/downloads.html)
```bash
echo "POSTGRES_USERNAME=<your_db_username>" >> .env
echo "POSTGRES_PASSWORD=<your_db_password>" >> .env

alembic upgrade head # Apply db migrations
```
- Generate [OpenAI API Key](https://platform.openai.com/docs/quickstart)
```bash
echo "OPENAI_API_KEY=<your_api_key_here>" >> .env
```

- Run the server locally at [localhost](http://localhost:8000) 
```bash
python3 app/main.py
```

## API
Use [Postman Collection](docs/postman.json) to run the API
- Create user `/api/v1/auth/register`
```bash
curl -XPOST 'http://localhost:8000/api/v1/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_name": "John Doe",
    "user_age": 42,
    "user_password": "abcd1234",
    "user_email": "abcd@xyz.com"
}'
```
- Create journal entrys `/api/v1/journal/create`
```bash
curl -XPOST 'http://localhost:8000/api/v1/journal/create' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": 0,
    "content": "Today was a very good day",
    "date": "2024-12-08"
}'

curl -XPOST 'http://localhost:8000/api/v1/journal/create' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": 0,
    "content": "Today was a bad day",
    "date": "2024-12-07"
}'
```
- Summarise with LLM `/api/v1/summarise`
```bash
curl -XPOST 'http://localhost:8000/api/v1/llm/summarise' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": 0,
    "days": [
        "2024-12-08",
        "2024-12-06"
    ]
}'
```

