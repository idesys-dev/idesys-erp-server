

DOCKER_COMPOSE = docker-compose

.env:
ifeq (,$(wildcard ./.env))
	cp .env.dist .env
endif

##
## Project
## -------
##
start: .env  ## Start the development server
	$(DOCKER_COMPOSE) up

start-d: .env  ## Start the development server (silent)
	$(DOCKER_COMPOSE) up -d

stop: ## Stop the project
	$(DOCKER_COMPOSE) down

kill: ## Kill the project
	$(DOCKER_COMPOSE) kill

build: ## Build the project
	$(DOCKER_COMPOSE) build

console: ## Open a console 
	$(DOCKER_COMPOSE) exec -T server sh

.PHONY: start
.DEFAULT_GOAL := help
help:
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
.PHONY: help
