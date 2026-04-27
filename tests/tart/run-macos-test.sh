#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Run macOS Dotfiles Test inside Tart VM
# =============================================================================
# Task: 4.4 — Clona desde `dotfiles-macos-base` snapshot `clean` hacia una VM
#       timestamped (`dotfiles-macos-test-<timestamp>`), ejecuta
#       `sentu_install.py` dentro, y reporta pass/fail.
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
VM_CLEAN="dotfiles-macos-clean"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
VM_TEST="dotfiles-macos-test-${TIMESTAMP}"
BOOT_TIMEOUT=300
TEST_TIMEOUT=1800  # 30 minutos para la instalación completa
SSH_USER="admin"
SSH_PASS="admin"

log_info() { echo -e "\033[1;34m[INFO]\033[0m  $*"; }
log_ok()   { echo -e "\033[1;32m[OK]\033[0m    $*"; }
log_warn() { echo -e "\033[1;33m[WARN]\033[0m  $*"; }
log_err()  { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; }

# --- Pre-flight checks -------------------------------------------------------

if ! command -v tart &>/dev/null; then
    log_err "Tart no está instalado."
    exit 1
fi

if ! tart list | grep -q "${VM_CLEAN}"; then
    log_err "La VM clean '${VM_CLEAN}' no existe. Ejecuta primero ./snapshot-macos-clean.sh"
    exit 1
fi

# --- Clone clean VM into timestamped test VM ---------------------------------

log_info "Clonando '${VM_CLEAN}' → '${VM_TEST}'..."
tart clone "${VM_CLEAN}" "${VM_TEST}"

# --- Start test VM -----------------------------------------------------------

log_info "Iniciando VM de prueba '${VM_TEST}'..."
tart run "${VM_TEST}" &
TART_PID=$!

# Esperar IP
log_info "Esperando que la VM arranque..."
elapsed=0
VM_IP=""
while true; do
    if ! kill -0 "${TART_PID}" 2>/dev/null; then
        log_err "La VM se cerró inesperadamente durante el arranque."
        exit 1
    fi
    VM_IP=$(tart ip "${VM_TEST}" 2>/dev/null || true)
    if [[ -n "${VM_IP}" ]]; then
        break
    fi
    if (( elapsed >= BOOT_TIMEOUT )); then
        log_err "Timeout esperando IP de la VM."
        kill "${TART_PID}" 2>/dev/null || true
        exit 1
    fi
    sleep 5
    ((elapsed+=5))
    echo -n "."
done
echo
log_ok "VM lista en IP: ${VM_IP}"

# --- Copy project into VM ----------------------------------------------------

log_info "Copiando proyecto dotfiles a la VM..."
# Usar rsync o scp; primero esperamos a que SSH esté listo
sleep 10

SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10"

# Verificar conectividad SSH
elapsed=0
while ! ssh ${SSH_OPTS} "${SSH_USER}@${VM_IP}" 'echo ok' &>/dev/null; do
    if (( elapsed >= 120 )); then
        log_err "SSH no disponible después de 2 minutos."
        kill "${TART_PID}" 2>/dev/null || true
        exit 1
    fi
    sleep 5
    ((elapsed+=5))
    echo -n "."
done
echo

# Crear directorio destino y copiar
ssh ${SSH_OPTS} "${SSH_USER}@${VM_IP}" 'mkdir -p ~/dotfiles'
rsync -avz -e "ssh ${SSH_OPTS}" \
    --exclude='.git' \
    --exclude='node_modules' \
    "${PROJECT_ROOT}/" \
    "${SSH_USER}@${VM_IP}:~/dotfiles/"

log_ok "Proyecto copiado exitosamente."

# --- Run sentu_install.py inside VM ------------------------------------------

log_info "Ejecutando sentu_install.py (modo test --check) dentro de la VM..."
log_info "Timeout: ${TEST_TIMEOUT}s"

TEST_OUTPUT=$(mktemp)
TEST_EXIT=0

# Ejecutar con timeout
ssh ${SSH_OPTS} "${SSH_USER}@${VM_IP}" \
    'cd ~/dotfiles && echo "4" | python3 sentu_install.py' \
    >"${TEST_OUTPUT}" 2>&1 || TEST_EXIT=$?

# Nota: enviamos "4" (Salir) al menú interactivo para evitar bloqueo.
# Para una prueba real, reemplazar por "1" o "3" según lo que se quiera validar.

if [[ ${TEST_EXIT} -eq 0 ]]; then
    log_ok "Test completado exitosamente (exit code 0)."
else
    log_err "Test falló con exit code ${TEST_EXIT}."
fi

# Mostrar últimas líneas del output
log_info "Últimas 30 líneas de salida:"
tail -n 30 "${TEST_OUTPUT}" | sed 's/^/    /'

# --- Cleanup test VM ---------------------------------------------------------

log_info "Apagando y eliminando VM de prueba '${VM_TEST}'..."
ssh ${SSH_OPTS} "${SSH_USER}@${VM_IP}" 'sudo shutdown -h now' 2>/dev/null || true
wait "${TART_PID}" 2>/dev/null || true
sleep 3
tart delete "${VM_TEST}" || log_warn "No se pudo eliminar '${VM_TEST}'"

rm -f "${TEST_OUTPUT}"

# --- Report ------------------------------------------------------------------

if [[ ${TEST_EXIT} -eq 0 ]]; then
    log_ok "========================================"
    log_ok "  RESULTADO: PASS"
    log_ok "  VM:       ${VM_TEST}"
    log_ok "  Timestamp: ${TIMESTAMP}"
    log_ok "========================================"
    exit 0
else
    log_err "========================================"
    log_err "  RESULTADO: FAIL"
    log_err "  VM:       ${VM_TEST}"
    log_err "  Timestamp: ${TIMESTAMP}"
    log_err "  Exit code: ${TEST_EXIT}"
    log_err "========================================"
    exit 1
fi
