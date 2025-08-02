start_localdb:
	python scripts/generate_env_from_dynaconf.py
	docker compose -f docker-compose.localdb.yml up -d

test:
	@EXIT_CODE=0; \
	docker compose -f docker-compose-test.yml build app-test && \
	docker compose -f docker-compose-test.yml run --rm app-test || EXIT_CODE=$$?; \
	docker compose -f docker-compose-test.yml down --volumes; \
	exit $$EXIT_CODE