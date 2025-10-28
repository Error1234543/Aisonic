FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV BOT_TOKEN=""
ENV OPENAI_API_KEY=""

HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1

CMD ["python", "main.py"]
