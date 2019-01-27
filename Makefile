ROOT=$(abspath $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))
IMAGE=fopina/kdbxpasswordpwned

build:
	docker build -t $(IMAGE) .

push: 
	docker push $(IMAGE):latest

travis-tag: build dockertest push
	docker tag $(IMAGE) $(IMAGE):$(TAG)
	docker push $(IMAGE):$(TAG)

travis-dev: build dockertest
	docker tag $(IMAGE) $(IMAGE):dev
	docker push $(IMAGE):dev

test:
	coverage run tests.py
	coverage report

dockertest: build
	docker run --rm -ti $(IMAGE) -h
	echo "reallysafeone" | docker run --rm -i \
			   -v $(ROOT)/test_assets/sample_with_key.kdbx:/tmp.kdbx:ro \
               -v $(ROOT)/test_assets/sample.key:/tmp.key:ro \
               $(IMAGE) \
               -upk /tmp.key /tmp.kdbx

pypi:
	python setup.py sdist upload

pypitest:
	python setup.py sdist upload -r https://test.pypi.org/legacy/


.PHONY: push build travis-dev travis-tag test dockertest pypi pypitest