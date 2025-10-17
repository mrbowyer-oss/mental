FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PLAYWRIGHT_BROWSERS_PATH=0

WORKDIR /app

# Install system packages and Chromium
RUN apt-get update && apt-get install -y     wget     gnupg     curl     fonts-liberation     libappindicator3-1     libasound2     libatk-bridge2.0-0     libatk1.0-0     libcups2     libdbus-1-3     libgdk-pixbuf2.0-0     libnspr4     libnss3     libx11-xcb1     libxcomposite1     libxdamage1     libxrandr2     libu2f-udev     xdg-utils     chromium     --no-install-recommends &&     apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application files
COPY . .

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
