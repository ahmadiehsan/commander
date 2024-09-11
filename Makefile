# =========================
# Init
# =====
ARGS := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARGS):;@:)  # Change the target-level arguments into do-nothing targets

# =========================
# Help (Put it first so that "make" without argument is like "make help")
# =====
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z0-9][a-zA-Z0-9._-]*:' Makefile | sort | awk -F: '{print "  "$$1}'

# =========================
# PreCommit
# =====
pre_commit.init:
	pre-commit install
	pre-commit install --hook-type pre-push
	pre-commit install --hook-type commit-msg

pre_commit.run_for_all:
	pre-commit run --all-files

# =========================
# Requirements
# =====
requirements.compile:
	rm -f requirements/compiled/*.txt
	pip install -r requirements/prerequisite/pip-tools.txt
	pip-compile -v requirements/raw/dev.in -o requirements/compiled/dev.txt

requirements.install:
	pip install -r requirements/prerequisite/pip-tools.txt
	pip-sync requirements/compiled/dev.txt
