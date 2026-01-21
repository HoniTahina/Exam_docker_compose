COMPOSE=docker-compose

.PHONY: up down purge-db purge-all restart

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

purge-db:
	$(COMPOSE) down
	docker volume rm $$(docker volume ls -q | grep postgres) || true

purge-all:
	$(COMPOSE) down -v --rmi all --remove-orphans
	docker system prune -af
	rm -rf node_modules dist build .cache

re: purge-all up
