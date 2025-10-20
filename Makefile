install:
	pip install -e .

list:
	agi-protei list-plugins

invoke-echo:
	agi-protei invoke --tool echo --text "hello"

invoke-add:
	agi-protei invoke --tool math.add --a 1 --b 2
