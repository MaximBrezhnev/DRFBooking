start_localdb:
	python scripts/generate_env_from_dynaconf.py
	docker compose -f docker-compose.localdb.yml --profile dev up -d