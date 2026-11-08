ARG PHP_BASE=php:8.4.26-apache@sha256:b0ae0e0d4a3b7f0e800017482752b94f58ab049f2d7fcd108e5452afce3f50d1
FROM ${PHP_BASE}
ARG PHP_CONFIG=vulnerable.ini
LABEL org.opencontainers.image.title="AtlaHub Zaatra University Lab" org.opencontainers.image.vendor="AtlaHub Tech"
COPY www/ /var/www/html/
COPY config/${PHP_CONFIG} /usr/local/etc/php/conf.d/zz-php2shell-lab.ini
COPY config/servername.conf /etc/apache2/conf-enabled/zz-php2shell-servername.conf
COPY config/apache-single-worker.conf /etc/apache2/conf-enabled/zz-php2shell-single-worker.conf
COPY evidence/ /opt/atlahub-training/
COPY LICENSE NOTICE /usr/share/doc/atlahub-upstream/
RUN mkdir -p /out && chown www-data:www-data /out && chmod 0755 /opt/atlahub-training && chmod 0644 /opt/atlahub-training/*
HEALTHCHECK --interval=3s --timeout=2s --start-period=5s --retries=20 CMD kill -0 1 && (grep -q ':0050 ' /proc/net/tcp || grep -q ':0050 ' /proc/net/tcp6)
