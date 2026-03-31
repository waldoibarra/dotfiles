## ╔════════════════════════════════════════════════════════════════════╗
## ║                  See the README.md file for usage                  ║
## ╚════════════════════════════════════════════════════════════════════╝

help: ## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

brew-dump: ## Dump all installed packages into the global Brewfile.
	brew bundle dump --global --force --describe

brew-cleanup: ## Cleanup anything that's not in the global Brewfile.
	brew bundle cleanup --global --force

brew-upgrade: ## Upgrade all items in the global Brewfile.
	brew bundle upgrade --global

install:
	./install.sh

check: ## Use ShellCheck to check for bugs on shell scripts.
	shellcheck scripts/restart-brew-service-with-custom-plist.sh
	shellcheck scripts/update-opencode-config.sh

update-oc: ## Update OpenCode configuration.
	./scripts/update-opencode-config.sh
