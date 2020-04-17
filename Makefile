all:

clean:
	find -name "*.pyc" -type f -delete
	find -name "__pycache__" -type d -delete

pyflakes:
	@echo Running pyflakes...
	@pyflakes3 */*.py

pydocstyle:
	@echo Running pydocstyle...
	@pydocstyle

pycodestyle:
	@echo Running pycodestyle...
	@pycodestyle --ignore=E501 */*.py

codespell:
	@echo Running codespell...
	@codespell */*.py

lint:
	@echo Running pylint...
	@pylint --rcfile=.pylintrc */*.py

unittest:
	@echo Running unit tests...
	@python3 -m unittest tests/*.py

test: pycodestyle pydocstyle pyflakes lint codespell unittest
