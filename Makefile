.PHONY: api

api:
	cd apps/api && uv run fastapi dev