FROM python:3.9-slim
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir openai-whisper flask gunicorn
WORKDIR /app
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]
