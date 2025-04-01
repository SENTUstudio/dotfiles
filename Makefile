.DEFAULT_GOAL := help

logo:
	clear
	@echo ""
	@echo "  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤  Ingeniería de Datos & Data Science  ├┒"
	@echo "  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤              en Python               ├┚"
	@echo "              .studio"
	@echo ""

## display help message
help: logo
	@awk '/^##.*$$/,/^[~\/\.0-9a-zA-Z_-]+:/' $(MAKEFILE_LIST) | awk '!(NR%2){print $$0p}{p=$$0}' | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sort

SCRIPT_URL = https://raw.githubusercontent.com/SENTUstudio/dotfiles/refs/heads/develop/sentu_install.py

## Ejecuta la prueba del script en un contenedor Docker de openSUSE Tumbleweed
test-opensuse:
	@echo "Ejecutando prueba en contenedor Docker de openSUSE..."
	docker run --rm opensuse/tumbleweed sh -c 'zypper refresh && zypper --non-interactive install python3 && curl -LsSf "${SCRIPT_URL}" | python3'
	@echo "Prueba finalizada."
