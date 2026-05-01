FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .[dev]

COPY . .

VOLUME ["/app/EmojiSaverBot.db"]

CMD ["python", "main.py"]
