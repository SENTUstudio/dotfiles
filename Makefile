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
USERNAME = el
PASSWORD = el

## Chequea el proyecto ansible con detalles
ansible-check: logo
	ansible-playbook \
		--ask-become-pass \
		--check ansible/playbook.yml \
		-i ansible/inventory.ini \
		-v

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
	" > logs/ansible.log

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
	" > logs/ansible.log

## Ejecuta la prueba del script en un contenedor Docker de Archlinux
test-archlinux: logo
	@echo "Ejecutando prueba en contenedor Docker de Archlinux..."
	# Asegurarse de que el directorio logs existe
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
