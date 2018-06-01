#!/usr/bin/make
.PHONY: buildout cleanall test instance

bin/pip:
	virtualenv-2.7 .
	touch $@

bin/buildout: buildout.cfg bin/pip
	./bin/pip install -I -r requirements.txt
	touch $@

buildout: bin/buildout
	./bin/buildout -t 7

test: buildout
	./bin/test

instance: buildout
	./bin/instance fg

cleanall:
	rm -rf bin develop-eggs downloads include lib parts .installed.cfg .mr.developer.cfg bootstrap.py parts/omelette
