FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3002

RUN mkdir -p instance

CMD ["python", "app.py"]