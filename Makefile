all:

style-check:
	black --diff --check pdf2images bin tests
	flake8 --ignore E501,E203,F401,W503,W504 --radon-max-cc 13 pdf2images bin tests

test:
	mkdir -p test-results
	python3 -m pytest \
	    --cov=pdf2images \
	    --no-cov-on-fail \
	    --cov-report=html:test-results/htmlcov \
	    --cov-report term \
	    --doctest-modules \
	    --junitxml=test-results/junit.xml \
	    pdf2images tests

wheel:
	python3 setup.py sdist bdist_wheel
