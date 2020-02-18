FROM python:3.8-alpine

RUN adduser -D homedash

WORKDIR /home/homedash

RUN apk update
RUN apk add --virtual build-dependencies gcc

#Pillow Requeirments
RUN apk add --no-cache libffi-dev openssl-dev

#Pillow Requeirments
RUN apk --no-cache add linux-headers \
                        libc-dev \
                       musl-dev \
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev


COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY homedash.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP homedash.py

RUN chown -R homedash:homedash ./
USER homedash

EXPOSE 5000
EXPOSE 45321
ENTRYPOINT ["./boot.sh"]