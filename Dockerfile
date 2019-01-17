FROM python:2.7-alpine3.8

WORKDIR /app
ADD requirements.txt /app/
RUN apk add --no-cache --virtual .build-deps \
								 libxml2-dev \
								 build-base \
								 libxslt-dev && \
	pip install -r /app/requirements.txt && \
	apk del .build-deps
RUN apk add --no-cache libxslt
ADD *.py /app/

ENTRYPOINT [ "/app/kdbxpasswordpwned.py" ]
