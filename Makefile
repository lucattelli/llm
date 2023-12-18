clean:
	rm -rf venv
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	make install

format:
	. venv/bin/activate; isort myrag; black myrag

install:
	test -d venv || python3 -m venv venv
	. venv/bin/activate; pip install --upgrade pip; pip install -r requirements.txt

lint:
	. venv/bin/activate; pylint --rc-file .pylintrc myrag

test:
	. venv/bin/activate; pytest tests
