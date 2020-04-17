all:

clean:
	find -name "*.pyc" -type f -delete
	find -name "__pycache__" -type d -delete

pyflakes:
	@echo Running pyflakes...
	@pyflakes3 pad */*.py

pydocstyle:
	@echo Running pydocstyle...
	@pydocstyle

pycodestyle:
	@echo Running pycodestyle...
	@pycodestyle --ignore=E501 pad */*.py

codespell:
	@echo Running codespell...
	@codespell pad */*.py

lint:
	@echo Running pylint...
	@pylint3 --rcfile=.pylintrc pad */*.py

unittest:
	@echo Running unit tests...
	@python3 -m unittest tests/*.py

test: pycodestyle pydocstyle pyflakes lint codespell unittest
