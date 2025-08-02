start_localdb:
	python scripts/generate_env_from_dynaconf.py
	docker compose -f docker-compose.localdb.yml up -d

test:
	export ENV_FOR_DYNACONF=test
	python scripts/generate_env_from_dynaconf.py
	docker compose -f docker-compose-test.yml up --build --abort-on-container-exit
