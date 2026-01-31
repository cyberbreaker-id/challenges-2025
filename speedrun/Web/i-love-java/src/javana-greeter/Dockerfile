FROM eclipse-temurin:11-jdk

WORKDIR /app

COPY target/javana-greeter-1.0.0.jar app.jar

EXPOSE 8081

ENTRYPOINT ["java", "-jar", "app.jar"]
