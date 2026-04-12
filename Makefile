.PHONY: build-surfaces build-surfaces-dry-run

# Regenerate all 4 distribution surfaces from the capability registry.
# See specs/055-capability-registry.md section 3.4.
build-surfaces:
	python scripts/build-surfaces.py
	@echo "Surfaces regenerated. Verify with: pytest && conversus --help"

# Print what would change without writing files — safe to run anytime.
build-surfaces-dry-run:
	python scripts/build-surfaces.py --dry-run
