FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY sitevault/requirements.txt requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "sitevault.app:app"]
