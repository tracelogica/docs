FROM python:3.12.11-alpine3.22 AS builder

WORKDIR /src
COPY README.md CONTRIBUTING.md SECURITY.md site.py ./
COPY docs ./docs
COPY assets ./assets
COPY web ./web
RUN python3 site.py build

FROM nginxinc/nginx-unprivileged:1.29.1-alpine3.22

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /src/site /usr/share/nginx/html

USER 101:101
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
