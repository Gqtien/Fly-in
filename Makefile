PYTHON		?= python3
VENV_DIR	?= .venv
BIN			:= $(VENV_DIR)/bin
UV			:= uv

MAKEFLAGS	:= --no-print-directory

DEPS		:= arcade
DEPSFLAG	:= $(VENV_DIR)/.installed

run:
	$(ensure_env)
	@$(BIN)/$(PYTHON) src/fly_in.py || true

install:
	@$(MAKE) clean
	@$(UV) venv $(VENV_DIR)
	@$(UV) pip install --upgrade pip --quiet
	@$(UV) pip install $(DEPS) --quiet
	@$(UV) pip install flake8 mypy --quiet
	@touch $(DEPSFLAG)
	@echo "Everything has been installed."
	@echo "You can now run 'make'"

debug:
	$(ensure_env)
	@$(BIN)/$(PYTHON) src/fly_in.py --debug || true

clean:
	@rm -rf $(VENV_DIR)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@rm -f profile.prof $(DEPSFLAG)

lint:
	$(ensure_env)
	@$(BIN)/$(PYTHON) -m flake8 src || true
	@$(BIN)/$(PYTHON) -m mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs || true

lint-strict:
	$(ensure_env)
	@$(BIN)/$(PYTHON) -m flake8 src || true
	@$(BIN)/$(PYTHON) -m mypy src --strict || true

define ensure_env
	@if [ ! -x "$(BIN)/python" -o ! -x "$(BIN)/pip" ]; then \
	    echo "Virtual environment not found. Installing..."; \
	    $(MAKE) install > /dev/null 2>&1; \
	fi
	@if [ ! -f "$(DEPSFLAG)" ]; then \
	    echo "Checking dependencies..."; \
	    missing=$$(for pkg in $(DEPS) mlx; do \
	        $(BIN)/pip list --format=freeze | grep -i "^$${pkg}==" >/dev/null || echo $$pkg; \
	    done); \
	    if [ -n "$$missing" ]; then \
	        echo "Missing dependencies: $$missing. Installing..."; \
	        $(MAKE) install > /dev/null 2>&1; \
	    fi; \
	fi
endef

.PHONY: run install debug clean lint lint-strict
