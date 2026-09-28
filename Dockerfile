FROM nginxinc/nginx-unprivileged:stable-alpine

COPY --chown=nginx:nginx . /usr/share/nginx/html/

EXPOSE 8080