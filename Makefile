.PHONY: tests
tests:
	py.test graphql_auth --cov=graphql_auth -vv

.PHONY: test
test: tests  # Alias test -> tests
