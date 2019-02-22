VERSION := $(shell grep __version__ pytan3/version.py | cut -d\" -f2)

.PHONY: docs build
env_init:
	pipenv install --dev --skip-lock

env_reset:
	$(MAKE) clean_env
	$(MAKE) env_init

pip_upgrade:
	pip --version
	python --version
	pip install --upgrade pip disttools pipenv

flake:
	pip install --quiet --upgrade flake8
	flake8 --max-line-length 100 --max-complexity=10 pytan3

black:
	pip install --quiet --upgrade black
	black pytan3 docs

test:
	pipenv run pytest --capture=no --showlocals --log-cli-level=DEBUG --verbose --exitfirst pytan3/tests

test_coverage:
	pipenv run pytest --junitxml=junit-report.xml --cov-config=.coveragerc --cov-report=term --cov-report xml --cov-report=html:cov_html --cov=pytan3 --capture=no --showlocals --log-cli-level=DEBUG --verbose --exitfirst pytan3/tests

test_all:
	@$(MAKE) check_env
	pyenv local 3.7.2
	$(MAKE) env_reset
	$(MAKE) test
	pyenv local 3.7.1
	$(MAKE) env_reset
	$(MAKE) test
	pyenv local 3.7.0
	$(MAKE) env_reset
	$(MAKE) test
	pyenv local 2.7.15
	$(MAKE) env_reset
	$(MAKE) test
	pyenv local --unset
	$(MAKE) env_reset

check_env:
	@if test "$(PYTAN_URL)" = ""; then echo "** Set PYTAN_URL variable first"; false ; fi
	@if test "$(PYTAN_USERNAME)" = ""; then echo "** Set PYTAN_USERNAME variable first"; false ; fi
	@if test "$(PYTAN_PASSWORD)" = ""; then echo "** Set PYTAN_PASSWORD variable first"; false ; fi

docs:
	$(MAKE) env_init
	pushd docs && pipenv run pip install --quiet --upgrade --requirement requirements.txt && pipenv run make html SPHINXOPTS="-na" && popd
	open docs/_build/html/index.html

docs_coverage:
	$(MAKE) env_init
	(pushd docs && pipenv run pip install --quiet --upgrade --requirement requirements.txt && pipenv run make coverage && popd) || true
	cat _build/coverage/python.txt

docs_linkcheck:
	$(MAKE) env_init
	(pushd docs && pipenv run pip install --quiet --upgrade --requirement requirements.txt && pipenv run make linkcheck && popd) || true
	cat docs/_build/linkcheck/output.txt

build:
	$(MAKE) lint
	$(MAKE) clean_dist

	pipenv run pip install --quiet --upgrade --requirement requirements-build.txt

	# Building Source and Wheel (universal) distribution…
	pipenv run python setup.py sdist bdist_wheel --universal

	# twine checking
	pipenv run twine check dist/*

clean_files:
	find . -type d -name "__pycache__" | xargs rm -rf
	find . -type f -name ".DS_Store" | xargs rm -f
	find . -type f -name "*.pyc" | xargs rm -f

clean_docs:
	rm -rf docs/_build

clean_env:
	pipenv --rm || true

clean_dist:
	rm -rf build dist pytan3.egg-info

clean_test:
	rm -rf .egg .eggs junit-report.xml cov_html .tox .pytest_cache .coverage

clean_all:
	$(MAKE) clean_dist
	$(MAKE) clean_files
	$(MAKE) clean_test
	$(MAKE) clean_env
	$(MAKE) clean_docs

git_check:
	# checking for version tag
	@git tag | grep "v$(VERSION)" || (echo "no tag for 'v$(VERSION)'"; false)
	# checking if repo has any changes
	git status

git_tag:
	@git tag "v$(VERSION)"
	@echo Added tag: v$(VERSION), now do:
	@echo git push --tags

publish:
	$(MAKE) git_check
	$(MAKE) build
	pipenv run python setup.py upload
