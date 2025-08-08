start_localdb:
	poetry run python scripts/generate_env_from_dynaconf.py
	docker compose -f docker-compose.localdb.yml up -d

test:
	@EXIT_CODE=0; \
	python scripts/generate_env_from_dynaconf.py
	docker compose -f docker-compose-test.yml build app-test && \
	docker compose -f docker-compose-test.yml run --rm app-test || EXIT_CODE=$$?; \
	docker compose -f docker-compose-test.yml down --volumes; \
	exit $$EXIT_CODE
dev:
	poetry run python scripts/generate_env_from_dynaconf.py
	docker compose up --build