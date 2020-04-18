all:

style-check:
	python3 -m black --diff --check pdf2images bin tests
	python3 -m flake8 --ignore E501,E203,F401,W503,W504 --radon-max-cc 13 pdf2images bin tests

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
	python3 -m coverage xml -o test-results/coverage.xml

wheel:
	python3 setup.py sdist bdist_wheel
