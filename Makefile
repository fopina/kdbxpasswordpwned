ROOT=$(abspath $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))
IMAGE=fopina/kdbxpasswordpwned

build:
	docker build -t $(IMAGE) .

push: 
	docker push $(IMAGE):latest

travis-tag: build push
	docker tag $(IMAGE) $(IMAGE):$(TAG)
	docker push $(IMAGE):$(TAG)

travis-dev: build
	docker tag $(IMAGE) $(IMAGE):dev
	docker push $(IMAGE):dev

test:
	coverage run tests.py
	coverage report

dockertest: build
	docker run --rm -ti $(IMAGE) -h


.PHONY: push build travis-dev travis-tag test dockertest