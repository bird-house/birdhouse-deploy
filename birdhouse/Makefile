## -- Lifecycle targets ----------------------------------------------------------------------------------------------- ##

.PHONY: configure
configure:			## One-off command to configure the stack
	echo "No configuration provided, skipping.."

.PHONY: start
start:			## Start the stack
	./pavics-compose.sh pull
	./pavics-compose.sh up -d

.PHONY: restart
restart:			## Restart the whole stack
	$(MAKE) stop
	$(MAKE) start

.PHONY: stop
stop:			## Stop the stack
	./pavics-compose.sh down

.PHONY: clean
clean:			## One-off command to clean the stack
	./pavics-compose.sh rm -vf

## -- Helper targets ----------------------------------------------------------------------------------------------- ##

.PHONY: compose
compose:			## Directly run commands against `pavics-compose.sh` script
	./pavics-compose.sh $(CMD)

.PHONY: help
help:			## Display this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
