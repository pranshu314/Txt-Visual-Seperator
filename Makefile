.SILENT:
.PHONY: winter
winter:
	python3 src/main.py /Users/pranshu/Projects/testline-assignment/images/winter.jpg

.SILENT:
.PHONY: person
person:
	python3 src/main.py /Users/pranshu/Projects/testline-assignment/images/person.jpg

.PHONY: run
run:
	python3 src/main.py $(FILE)
