FROM alpine:3.8

WORKDIR /app
ADD requirements.txt /app/
RUN apk add --no-cache py2-pip py2-lxml py2-cffi
RUN apk add --no-cache --virtual .build-deps \
								 build-base \
								 python2-dev && \
	pip install -r /app/requirements.txt && \
	apk del .build-deps

ADD *.py /app/

ENTRYPOINT [ "/app/kdbxpasswordpwned.py" ]
