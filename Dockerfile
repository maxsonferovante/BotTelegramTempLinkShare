FROM python:3.11.7-alpine3.19
LABEL authors="maal"

WORKDIR /app

COPY . .

RUN python3 -m venv venv
RUN /bin/sh -c "source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pip install python-telegram-bot --upgrade"


CMD ["python", "main.py"]


