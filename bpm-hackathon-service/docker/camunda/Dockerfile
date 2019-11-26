FROM maven:3-jdk-8 as builder
VOLUME /tmp
WORKDIR /workspace
COPY pom.xml .
COPY src ./src
RUN mvn -e -B package

FROM openjdk:8-jre-alpine
COPY --from=builder /workspace/target/test-service-0.0.1-SNAPSHOT.jar /test-service.jar
CMD ["java", "-jar", "test-service.jar"]