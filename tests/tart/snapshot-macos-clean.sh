#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Create Golden (Clean) Snapshot from Base VM
# =============================================================================
# Task: 4.3 — Crea un snapshot `clean` desde `dotfiles-macos-base` después del
#       boot inicial. Este es el golden snapshot para tests.
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VM_BASE="dotfiles-macos-base"
VM_CLEAN="dotfiles-macos-clean"
BOOT_TIMEOUT=300  # 5 minutos

log_info() { echo -e "\033[1;34m[INFO]\033[0m  $*"; }
log_ok()   { echo -e "\033[1;32m[OK]\033[0m    $*"; }
log_warn() { echo -e "\033[1;33m[WARN]\033[0m  $*"; }
log_err()  { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; }

# --- Pre-flight checks -------------------------------------------------------

if ! command -v tart &>/dev/null; then
    log_err "Tart no está instalado."
    exit 1
fi

if ! tart list | grep -q "${VM_BASE}"; then
    log_err "La VM base '${VM_BASE}' no existe. Ejecuta primero ./setup-macos-base.sh"
    exit 1
fi

if tart list | grep -q "${VM_CLEAN}"; then
    log_warn "La VM clean '${VM_CLEAN}' ya existe."
    read -rp "¿Eliminarla y recrear? [y/N]: " answer
    if [[ "${answer}" =~ ^[Yy]$ ]]; then
        tart delete "${VM_CLEAN}" || true
    else
        log_info "Usando VM clean existente. Salida."
        exit 0
    fi
fi

# --- Boot base VM once to let macOS finish first-run setup -------------------

log_info "Iniciando '${VM_BASE}' para completar setup inicial de macOS..."
log_info "(Esta ventana se cerrará automáticamente en ${BOOT_TIMEOUT}s)"

# Iniciar en background y capturar PID
tart run "${VM_BASE}" &
TART_PID=$!

# Esperar a que la VM esté lista (poll con tart ip)
log_info "Esperando que macOS termine configuración inicial..."
elapsed=0
while ! tart ip "${VM_BASE}" &>/dev/null; do
    if ! kill -0 "${TART_PID}" 2>/dev/null; then
        log_err "La VM se cerró inesperadamente."
        exit 1
    fi
    if (( elapsed >= BOOT_TIMEOUT )); then
        log_err "Timeout esperando que la VM arranque."
        kill "${TART_PID}" 2>/dev/null || true
        exit 1
    fi
    sleep 5
    ((elapsed+=5))
    echo -n "."
done
echo

log_ok "VM base arrancada y lista. Apagando para clonar..."

# Detener la VM base (graceful shutdown via SSH o kill)
# En imágenes de Cirrus, el usuario por defecto es 'admin' con password 'admin'
# Intentamos shutdown graceful
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    -o ConnectTimeout=5 \
    admin@"$(tart ip "${VM_BASE}")" \
    'sudo shutdown -h now' 2>/dev/null || true

# Esperar a que termine
wait "${TART_PID}" 2>/dev/null || true
sleep 5

# --- Clone into clean golden VM ----------------------------------------------

log_info "Clonando '${VM_BASE}' → '${VM_CLEAN}' (golden snapshot)..."
tart clone "${VM_BASE}" "${VM_CLEAN}"

log_ok "Golden snapshot '${VM_CLEAN}' creado exitosamente."
log_info "Usa ./run-macos-test.sh para lanzar tests desde este snapshot."
