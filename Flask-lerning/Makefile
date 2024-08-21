all: format_main format_recursion

format_main:
	autopep8 -i *.py

format_recursion:
	autopep8 -i */*.py

git:
	git add .
	git commit -m "make commit"
	git push

venv:
	source .venv/bin/activate