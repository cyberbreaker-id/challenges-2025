FROM openjdk:11-jdk-slim

WORKDIR /app

COPY pom.xml ./
COPY main ./src/main

RUN apt-get update && apt-get install -y maven curl && \
    mvn clean package -DskipTests && \
    mv target/spring-app-*.jar app.jar && \
    apt-get remove -y maven && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]