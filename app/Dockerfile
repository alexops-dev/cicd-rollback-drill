FROM python:3.14-slim

WORKDIR /app

COPY main.py .

ENV HOST=0.0.0.0 \
    PORT=8000 \
    PYTHONUNBUFFERED=1

USER 10001:10001

EXPOSE 8000

CMD ["python", "main.py"]