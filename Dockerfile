FROM python:2.7-alpine3.8

WORKDIR /app
ADD *.py requirements.txt /app/
RUN apk add --no-cache --virtual .build-deps \
								 libxml2-dev \
								 build-base \
								 libxslt-dev && \
	pip install -r /app/requirements.txt && \
	apk del .build-deps
RUN apk add --no-cache libxslt

ENTRYPOINT [ "/app/kdbxpasswordpwned.py" ]
