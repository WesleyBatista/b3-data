#!make 

.DEFAULT_GOAL := help


help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

patch-release: ## bump a patch version push/create tag and release
	@./release patch

minor-release: ## bump a minor version push/create tag and release
	@./release minor

major-release: ## bump a major version push/create tag and release
	@./release major
