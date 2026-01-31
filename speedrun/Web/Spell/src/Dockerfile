FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
# Convenience tools for RCE exfil during solve
RUN apt-get update -y && apt-get install -y --no-install-recommends curl netcat-traditional ca-certificates && rm -rf /var/lib/apt/lists/*
COPY ./target/spell-1.0.0.jar ./spell-1.0.0.jar
COPY flag.txt /flag.txt
RUN chmod 0644 /flag.txt
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/spell-1.0.0.jar"]
