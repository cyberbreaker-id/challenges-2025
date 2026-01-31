FROM golang:1.25 AS builder
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*
COPY . .
ENV CGO_ENABLED=1
RUN go build -o app

EXPOSE 3000

CMD ["./app"]
