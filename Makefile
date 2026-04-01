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
	shellcheck -a scripts/restart-brew-service-with-custom-plist.sh
	shellcheck -a scripts/update-coding-agents.sh

update-ca: ## Update coding agents.
	./scripts/update-coding-agents.sh
