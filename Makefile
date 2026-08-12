.PHONY: build serve test clean

build:
	python3 site.py build

serve:
	python3 site.py serve

test:
	python3 -m unittest discover -s tests -v

clean:
	rm -rf site
