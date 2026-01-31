FROM eclipse-temurin:11-jdk

WORKDIR /app

# Download jetty-runner
ADD https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-runner/9.4.53.v20231009/jetty-runner-9.4.53.v20231009.jar jetty-runner.jar

# Copy your WAR
COPY target/javana-1.0-SNAPSHOT.war app.war

EXPOSE 9001

ENTRYPOINT ["java", "-jar", "jetty-runner.jar", "--port", "9001", "app.war"]
