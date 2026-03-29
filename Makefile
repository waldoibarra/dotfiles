## ----------------------------------------------------------------------
## See the README.md file for usage.
## ----------------------------------------------------------------------

help: ## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

check: ## Use ShellCheck to check for bugs on shell scripts.
	shellcheck scripts/restart-brew-service-with-custom-plist.sh
	shellcheck scripts/update-opencode-config.sh

update-oc: ## Update OpenCode configuration.
	./scripts/update-opencode-config.sh
