FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libxrender1 libxext6 libsm6 libxrandr2 x11-xkb-utils xauth xfonts-base xfonts-75dpi xfonts-100dpi \
    libxtst6 libxss1 xdg-utils && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/app.py"]
