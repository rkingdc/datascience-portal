FROM nginx

RUN apt-get update && \
    apt-get install -y openssl
    
COPY nginx.conf /etc/nginx/nginx.conf

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/localhost.key -out /etc/nginx/localhost.crt -subj "/C=US/ST=CA/O=RKDC/OU=Shinyproxy/CN=localhost"

