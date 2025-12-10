# docker buildx build -f Dockerfile . -t pavics/nginx-cron-logrotate:1.23.4-251205 --pull --no-cache
FROM nginx:1.23.4

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --no-install-suggests -y cron logrotate && \
    apt-get clean
