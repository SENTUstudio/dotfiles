.DEFAULT_GOAL := help

logo:
	clear
	@echo ""
	@echo "   \033[1m\033[33m█▀ █▀▀ █▄░█ ▀█▀ █░█\033[0m  ┎┤ Ingeniería de Datos & Data Science ├┒"
	@echo "   \033[1m\033[33m▄█ ██▄ █░▀█ ░█░ █▄█\033[0m  ┖┤ \033[1m       Dotfiles Manager Go          \033[0m├┚"
	@echo "               .studio"
	@echo ""

## display help message
help: logo
	@awk '/^##.*$$/,/^[~\/\.0-9a-zA-Z_-]+:/' $(MAKEFILE_LIST) | awk '!(NR%2){print $$0p}{p=$$0}' | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}' | sort

# Variables
BINARY_NAME = sentu-dotfiles
CMD_PATH = ./cmd/sentu-dotfiles
SCRIPT_URL = https://raw.githubusercontent.com/SENTUstudio/dotfiles/refs/heads/develop/sentu_install.py
USERNAME = el
PASSWORD = el

# =============================================================================
# Go / sentu-dotfiles targets
# =============================================================================

## Build sentu-dotfiles binary for current platform
build: logo
	go build -ldflags="-s -w" -o $(BINARY_NAME) $(CMD_PATH)
	@echo ""
	@./$(BINARY_NAME) --version

## Run sentu-dotfiles in TUI mode
run: build
	./$(BINARY_NAME)

## Install sentu-dotfiles to ~/.local/bin
install: build
	mkdir -p $(HOME)/.local/bin
	cp $(BINARY_NAME) $(HOME)/.local/bin/$(BINARY_NAME)
	@echo "Installed to $(HOME)/.local/bin/$(BINARY_NAME)"

## Build releases for all platforms (linux/darwin x amd64/arm64)
release: logo
	@mkdir -p dist
	@echo "Building releases..."
	@for os in linux darwin; do \
		for arch in amd64 arm64; do \
			echo "  → $$os/$$arch"; \
			GOOS=$$os GOARCH=$$arch go build -ldflags="-s -w -X main.version=dev" \
				-o dist/$(BINARY_NAME)_$${os}_$${arch} $(CMD_PATH); \
			done; \
		done
	@echo ""
	@ls -lh dist/

## Clean build artifacts
clean:
	rm -f $(BINARY_NAME)
	rm -rf dist/

## Run Go tests
test:
	go test ./...

## Download Go dependencies
deps:
	go mod tidy

# =============================================================================
# Ansible targets
# =============================================================================

## Chequea el proyecto ansible con detalles
ansible-check: logo
	ansible-playbook \
		--ask-become-pass \
		--check ansible/playbook.yml \
		-i ansible/inventory.ini \
		-vvv \
		&> logs/ansible.log

# =============================================================================
# Docker test targets
# =============================================================================

## Ejecuta la prueba del script en un contenedor Docker de openSUSE Tumbleweed
test-opensuse: logo
	@echo "Ejecutando prueba en contenedor Docker de openSUSE..."
	docker run --rm opensuse/tumbleweed sh -c " \
		set -e; \
		zypper refresh; \
		zypper --non-interactive install which python3-pip python3 sudo; \
		useradd -m ${USERNAME}; \
		echo '${USERNAME}:${PASSWORD}' | chpasswd; \
		echo '%${USERNAME} ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers; \
		su - ${USERNAME} -c 'curl -LsSf \"${SCRIPT_URL}\" | python3'; \
	" &> logs/ansible.log

## Ejecuta la prueba del script en un contenedor Docker de Fedora
test-fedora: logo
	@echo "Ejecutando prueba en contenedor Docker de Fedora..."
	docker run --rm fedora sh -c " \
		set -e; \
		dnf update -y; \
		dnf install which python3-pip python3 sudo ansible -y; \
		useradd -m ${USERNAME}; \
		echo '${USERNAME}:${PASSWORD}' | chpasswd; \
		echo '%${USERNAME} ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers; \
		sudo -u el bash -c 'curl -LsSf \"${SCRIPT_URL}\" | python3'; \
	" &> logs/ansible.log

## Ejecuta la prueba del script en un contenedor Docker de Archlinux
test-archlinux: logo
	@echo "Ejecutando prueba en contenedor Docker de Archlinux..."
	mkdir -p logs
	docker run --rm archlinux sh -c " \
		set -e; \
		pacman -Suy --noconfirm; \
		pacman -Sy --needed --noconfirm which python-pip python3 sudo ansible; \
		useradd -m ${USERNAME}; \
		echo '${USERNAME}:${PASSWORD}' | chpasswd; \
		echo '%${USERNAME} ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers; \
		sudo -u ${USERNAME} bash -c 'curl -LsSf \"${SCRIPT_URL}\" | python3'; \
	" &> logs/ansible.log
	@echo "Prueba finalizada."
