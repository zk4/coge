.PHONY: version rm dev test coge auto_version upload-to-prod init requirements.txt pip

SOURCE_ENV = . venv/bin/activate

# Indicates each line of command in target would run in one shell ,
# only make file version >=3.8.2 support
.ONESHELL:

rm:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -type d -iname '*egg-info' -exec rm -rdf {} +
	rm -f .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	# rm -rf .py.egg-info
	rm -rf .pytest_cache
	rm -rf .hypothesis
	rm -rdf assets


test: rm
	watchexec -ce py 'pytest -s -v  tests/'

coverage-html:
	# --cov where you want to cover
	#  tests  where your test code is
	pytest --cov=coge/ --cov-report=html tests/
	open htmlcov/index.html

coverage:
	pytest --cov=coge/ tests/


install: uninstall
	pip3 install .

uninstall:
	pip3 uninstall  -y coge

main:
	python3 main.py eat -c 2


dev:
	# @python3 -m coge vue_template coge_name:vue_mall   coge_author:zk "Welcome to Your Vue.js App":'hello, coge'  @:vue_mall3 -w
	rm -rdf ap
	# @python  main.py  python cli @:hello
	@python main.py python3 -r files/Makfile


version:
	@python3 -m coge -v

run:
	# @python3 -m coge https://github.com/vitejs/vite \\bvite\\b:viteme  @:viteme -s
	@python3 -m coge git@github.com:zk4/webpack-demo webpack-demo:github-demo  @:github-demo -s  -b guide/webpack-dev-server

wrun:
	watchexec -ce py 'python3 -m coge eat -c 2'

all: rm uninstall install run


pure-all: env-rm rm env install test run



upload-to-test: rm
	python3 setup.py bdist_wheel --universal
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


upload-to-prod: rm auto_version
	python3 setup.py bdist_wheel --universal
	twine upload dist/*



freeze-env: auto_version
	#  pip3 will find all the module not belong to standard  library
	pip3 freeze > requirements.txt


env-rm:
	rm -rdf venv

env-create:
	python3 -m venv venv

env: env-create
	pip3 install -r requirements.txt


auto_version:
	python3 version.py

venv_rm:
	rm -rdf venv

venv: venv_rm
	python3 -m venv --clear venv
	pip install -r requirements.txt

requirements.txt:
	pip3 freeze > requirements.txt

