FROM openjdk:8-jre

RUN mkdir -p /opt/shinyproxy/
RUN wget https://www.shinyproxy.io/downloads/shinyproxy-2.1.0.jar -O /opt/shinyproxy/shinyproxy.jar

COPY application.yml /opt/shinyproxy/application.yml
COPY rk_favicon.png /opt/shinyproxy/favicon.png


WORKDIR /opt/shinyproxy/
CMD ["java", "-jar", "/opt/shinyproxy/shinyproxy.jar"]
