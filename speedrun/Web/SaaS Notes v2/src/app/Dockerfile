FROM golang:1.25 AS builder
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
ENV CGO_ENABLED=1
RUN go build -o app

FROM golang:1.25
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/app .
COPY --from=builder /app/static ./static
COPY .env .
COPY flag.txt .

EXPOSE 3000

CMD ["./app"]