# Makefile in the root of your project

.PHONY: notebook test build clean stop

# Start Jupyter notebooks using Docker Compose
notebook:
	docker compose -f docker/docker-compose.yml up --build

# Run tests from the local environment (e.g., inside Docker)
test:
	python -m unittest discover tests

stop:
	docker compose -f docker/docker-compose.yml down

# Build the Python package (Phase 2)
build:
	python setup.py sdist bdist_wheel

# Clean up build artifacts
clean:
	rm -rf dist build *.egg-info
