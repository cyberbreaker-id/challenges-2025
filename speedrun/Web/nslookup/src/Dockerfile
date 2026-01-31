# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install required tools (nslookup from dnsutils)
RUN apt-get update && \
    apt-get install -y dnsutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install
RUN pip install Flask

# Copy app and flag
COPY src/ .

USER nobody

ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
