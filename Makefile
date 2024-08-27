POETRY_VERSION = 1.3.2

APPLICATIONS := app-1 app-2
.DEFAULT_GOAL = help
export CURRENT_ENV = test

.PHONY: clean-parent
clean-parent: ## Remove distribution and report directories
	rm -rf dist
	rm -rf reports

.PHONY: clean
clean: clean-parent ## Clean all applications
	@for applications in $(APPLICATIONS); do \
  		${MAKE} -C applications/$$applications clean; \
  	done

.PHONY: dist-clean
dist-clean: clean-parent ## Deep clean all applications
	@for applications in $(APPLICATIONS); do \
  		${MAKE} -C applications/$$applications dist-clean; \
  	done

.PHONY: build
build: ## Build all applications
	@for applications in $(APPLICATIONS); do \
  		${MAKE} -C applications/$$applications build || FAILURES=$$(( $$FAILURES+1 )) ; \
  	done; \
  	exit $$(( $$FAILURES ))

.PHONY: update
update: ## Update all applications
	@for applications in $(APPLICATIONS); do \
  		${MAKE} -C applications/$$applications update || FAILURES=$$(( $$FAILURES+1 )) ; \
  	done; \
  	exit $$(( $$FAILURES ))

.PHONY: test
test: ## Test all applications
	@for applications in $(APPLICATIONS); do \
  		${MAKE} -C applications/$$applications test || FAILURES=$$(( $$FAILURES+1 )) ; \
  	done; \
  	exit $$(( $$FAILURES ))

.PHONY: cover
cover: ## Generate coverage reports for all applications
	@mkdir -p reports
	@for applications in $(APPLICATIONS); do \
  		${MAKE} -C applications/$$applications cover || FAILURES=$$(( $$FAILURES+1 )) ; \
  		mkdir -p reports/applications/$$applications; \
  		cp applications/$$applications/reports/* reports/applications/$$applications/; \
  	done; \
  	exit $$(( $$FAILURES ))

.PHONY: ssap
ssap: ## generate required reports for ssap
	@mkdir -p ssap-reports;
	@for applications in $(APPLICATIONS); do \
  	  	${MAKE} -C applications/$$applications ssap || FAILURES=$$(( $$FAILURES+1 )) ; \
  		cat applications/app-1/requirements.txt | sed -E '/file:\/\/\//d' >> ssap-reports/pip_dependency_tree.txt; \
  	done; \
  	exit $$(( $$FAILURES ))

.PHONY: package
package: ## Package all applications
	@mkdir -p dist
	@for application in $(APPLICATIONS); do \
  	  	${MAKE} -C applications/$$application package || FAILURES=$$(( $$FAILURES+1 )); \
  		cp applications/$$application/dist/package/applications.zip dist/$$application.zip; \
  	done; \
  	exit $$(( $$FAILURES ))

.PHONY: ci-prebuild
ci-prebuild: ## Install specified version of Poetry
	python -m pip install poetry==${POETRY_VERSION}

.PHONY: ci
ci: clean build package ## Clean, build, and package all applications

.PHONY: help
help: ## Show make target documentation
	@awk -F ':|##' '/^[a-zA-Z0-9_\-]+:.*##/ { \
	printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)
