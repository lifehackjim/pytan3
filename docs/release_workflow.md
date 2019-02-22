This all assumes dev on OSX. 

setup system packages
---------------------
```
pyenv shell 2.7.15
pip install -r requirements.txt
pip install -r requirements-dev.txt

pyenv shell 3.7.1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

reset pipenv
------------
```
make envreset || make envinit
```

lint
-----
```
make lint
```
* make black_do to perform changes

tests
-----
```
make cov_html
```
* opens cov_html/index.html for review

```
make test
```

* if errors, pytest in py2 and py3 manually

```
pyenv shell 2.7.15
make test

pyenv shell 3.7.1
make test
```

docs
-----
```
make docs
print docs/_build/coverage/python.txt
print docs/_build/linkcheck/output.txt
open docs/_build/html/index.html
```

build
------
```
make build
```

publish
--------
```
make publish
```
