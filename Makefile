.PHONY: setup install clean run lint format test help

PYTHON = python
PIP = pip

# Directories
SRC_DIR = src
VENV_DIR = venv

help:
	@echo "Available commands:"
	@echo "  make setup       - Create virtual environment and install dependencies"
	@echo "  make install     - Install dependencies only"
	@echo "  make run         - Run the video processor"
	@echo "  make lint        - Run linting"
	@echo "  make format      - Auto-format code with black"
	@echo "  make env         - Create .env file from example if it doesn't exist"

setup: $(VENV_DIR) env install

$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created at $(VENV_DIR)"

install: requirements.txt
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	pre-commit install
	@echo "Dependencies installed"

env:
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			cp .env.example .env; \
			echo ".env file created from example. Please edit with your actual API keys."; \
		else \
			echo "OPENAI_API_KEY=your-api-key-here" > .env; \
			echo "Created basic .env file. Please edit with your actual API keys."; \
		fi \
	else \
		echo ".env file already exists"; \
	fi

run: 
	$(PYTHON) main.py

lint:
	$(PYTHON) -m flake8 $(SRC_DIR)

format:
	@echo "Formatting Python code with Black..."
	@if ! command -v black &> /dev/null && ! $(PYTHON) -m black --version &> /dev/null; then \
		echo "black is not installed. Installing..."; \
		$(PIP) install black; \
	fi
	$(PYTHON) -m black --config pyproject.toml $(SRC_DIR)
	@echo "Black formatting complete."