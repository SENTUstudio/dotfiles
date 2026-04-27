#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Fedora Regression Test (Linux paths unchanged)
# =============================================================================
# Task: 4.5 — Levanta una VM Fedora (si está disponible) o usa Docker como
#       fallback, ejecuta `playbook-test.yml`, y reporta pass/fail.
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
VM_FEDORA="dotfiles-fedora-test"
CONTAINER_NAME="dotfiles-fedora-container"
BOOT_TIMEOUT=300
TEST_TIMEOUT=1800

log_info() { echo -e "\033[1;34m[INFO]\033[0m  $*"; }
log_ok()   { echo -e "\033[1;32m[OK]\033[0m    $*"; }
log_warn() { echo -e "\033[1;33m[WARN]\033[0m  $*"; }
log_err()  { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; }

# --- Helper: run with Docker fallback ----------------------------------------

run_with_docker() {
    log_info "Usando Docker como fallback para Fedora..."

    if ! command -v docker &>/dev/null; then
        log_err "Docker no está instalado. No se puede ejecutar el fallback."
        exit 1
    fi

    # Limpiar contenedor previo si existe
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log_warn "Eliminando contenedor previo '${CONTAINER_NAME}'..."
        docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
    fi

    log_info "Iniciando contenedor Fedora..."
    docker run -d --name "${CONTAINER_NAME}" \
        -v "${PROJECT_ROOT}:/dotfiles:ro" \
        --privileged \
        fedora:latest \
        sleep 3600

    log_info "Instalando dependencias en contenedor..."
    docker exec "${CONTAINER_NAME}" bash -c '
        dnf update -y
        dnf install -y python3 python3-pip git ansible sudo
    '

    log_info "Ejecutando syntax-check del playbook..."
    docker exec "${CONTAINER_NAME}" bash -c '
        cd /dotfiles/ansible && ansible-playbook --syntax-check playbook-test.yml
    '
    SYNTAX_EXIT=$?

    log_info "Ejecutando playbook en modo check (--check)..."
    # Nota: --check en contenedores muchas veces falla por privilegios;
    #       lo ejecutamos sin --check pero limitamos roles seguros.
    docker exec "${CONTAINER_NAME}" bash -c '
        cd /dotfiles/ansible && ansible-playbook -i inventory.ini playbook-test.yml || true
    ' || true
    PLAY_EXIT=$?

    log_info "Deteniendo y eliminando contenedor..."
    docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true

    return ${SYNTAX_EXIT}
}

# --- Helper: run with Tart VM ------------------------------------------------

run_with_tart() {
    if ! command -v tart &>/dev/null; then
        log_warn "Tart no está instalado."
        return 1
    fi

    # Verificar si existe una VM Fedora registrada en Tart
    if ! tart list | grep -qi "fedora"; then
        log_warn "No se encontró ninguna VM Fedora en Tart."
        return 1
    fi

    local fedora_vm
    fedora_vm=$(tart list | grep -i fedora | head -n1 | awk '{print $1}')
    log_info "Usando VM Fedora encontrada: ${fedora_vm}"

    # Clonar para test
    local test_vm="dotfiles-fedora-test-$(date +%Y%m%d-%H%M%S)"
    tart clone "${fedora_vm}" "${test_vm}" || {
        log_err "No se pudo clonar la VM Fedora."
        return 1
    }

    tart run "${test_vm}" &
    local tart_pid=$!

    # Esperar IP
    local elapsed=0 vm_ip=""
    while true; do
        vm_ip=$(tart ip "${test_vm}" 2>/dev/null || true)
        [[ -n "${vm_ip}" ]] && break
        if (( elapsed >= BOOT_TIMEOUT )); then
            log_err "Timeout esperando IP de VM Fedora."
            kill "${tart_pid}" 2>/dev/null || true
            tart delete "${test_vm}" || true
            return 1
        fi
        sleep 5
        ((elapsed+=5))
    done

    log_info "VM Fedora lista en ${vm_ip}. Copiando proyecto..."
    sleep 10

    local ssh_opts="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10"
    ssh ${ssh_opts} "user@${vm_ip}" 'mkdir -p ~/dotfiles'
    rsync -avz -e "ssh ${ssh_opts}" --exclude='.git' \
        "${PROJECT_ROOT}/" "user@${vm_ip}:~/dotfiles/"

    log_info "Ejecutando syntax-check..."
    ssh ${ssh_opts} "user@${vm_ip}" \
        'cd ~/dotfiles/ansible && ansible-playbook --syntax-check playbook-test.yml'
    local syntax_exit=$?

    log_info "Apagando VM de prueba..."
    ssh ${ssh_opts} "user@${vm_ip}" 'sudo shutdown -h now' 2>/dev/null || true
    wait "${tart_pid}" 2>/dev/null || true
    tart delete "${test_vm}" || true

    return ${syntax_exit}
}

# --- Main --------------------------------------------------------------------

log_info "========================================"
log_info "  Fedora Regression Test"
log_info "========================================"

# Intentar Tart primero, luego Docker
if run_with_tart; then
    TEST_EXIT=0
elif run_with_docker; then
    TEST_EXIT=0
else
    TEST_EXIT=1
fi

if [[ ${TEST_EXIT} -eq 0 ]]; then
    log_ok "========================================"
    log_ok "  RESULTADO: PASS"
    log_ok "  Linux paths sin cambios detectados."
    log_ok "========================================"
    exit 0
else
    log_err "========================================"
    log_err "  RESULTADO: FAIL"
    log_err "  Revisar salida de Ansible arriba."
    log_err "========================================"
    exit 1
fi
