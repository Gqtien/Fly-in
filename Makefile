PYTHON		?= python3
VENV_DIR	?= .venv
BIN			:= $(VENV_DIR)/bin
UV			:= uv

MAKEFLAGS	:= --no-print-directory

DEPS		:= arcade
DEPSFLAG	:= $(VENV_DIR)/.installed

usage:
	@echo "Usage: make <command>"
	@echo ""
	@echo "Commands:"
	@$(foreach cmd,$(filter-out usage,$(CMDS)), \
		echo "  - $(cmd)"

install:
	@$(MAKE) clean
	@$(UV) venv $(VENV_DIR)
	@$(UV) pip install --upgrade pip --quiet
	@$(UV) pip install $(DEPS) --quiet
	@$(UV) pip install flake8 mypy --quiet
	@touch $(DEPSFLAG)
	@echo "Everything has been installed."
	@echo "You can now run 'make run'"

run:
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
	        echo "Missing dependencies. Installing..."; \
	        $(MAKE) install > /dev/null 2>&1; \
	    fi; \
	fi
	@$(BIN)/$(PYTHON) src/fly_in.py $(ARGS) || true

# implement internal debug

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@rm -f profile.prof $(DEPSFLAG)

lint:
	@$(BIN)/$(PYTHON) -m flake8 src || true
	@$(BIN)/$(PYTHON) -m mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs || true

lint-strict:
	@$(BIN)/$(PYTHON) -m flake8 src || true
	@$(BIN)/$(PYTHON) -m mypy src --strict || true

$(ARGS):
	@:

.PHONY: usage install run profile debug clean lint lint-strict
