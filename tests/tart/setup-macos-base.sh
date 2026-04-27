#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Setup macOS Base VM for Tart Testing
# =============================================================================
# Task: 4.2 — Clone ghcr.io/cirruslabs/macos-sequoia-base:latest into
#       a local VM named `dotfiles-macos-base`.
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
VM_NAME="dotfiles-macos-base"
SOURCE_IMAGE="ghcr.io/cirruslabs/macos-sequoia-base:latest"

log_info() { echo -e "\033[1;34m[INFO]\033[0m  $*"; }
log_ok()   { echo -e "\033[1;32m[OK]\033[0m    $*"; }
log_warn() { echo -e "\033[1;33m[WARN]\033[0m  $*"; }
log_err()  { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; }

# --- Pre-flight checks -------------------------------------------------------

if ! command -v tart &>/dev/null; then
    log_err "Tart no está instalado. Instálalo con:"
    log_err "  brew install cirruslabs/cli/tart"
    exit 1
fi

if [[ "$(uname -m)" != "arm64" ]]; then
    log_warn "Tart solo funciona en Apple Silicon (arm64)."
    log_warn "Host detectado: $(uname -m)"
fi

# --- Clone base image --------------------------------------------------------

if tart list | grep -q "${VM_NAME}"; then
    log_warn "La VM '${VM_NAME}' ya existe."
    read -rp "¿Eliminarla y recrear? [y/N]: " answer
    if [[ "${answer}" =~ ^[Yy]$ ]]; then
        log_info "Eliminando VM existente '${VM_NAME}'..."
        tart delete "${VM_NAME}" || true
    else
        log_info "Usando VM existente. Salida."
        exit 0
    fi
fi

log_info "Clonando imagen base '${SOURCE_IMAGE}' → '${VM_NAME}'..."
log_info "Esto puede tardar varios minutos la primera vez."
tart clone "${SOURCE_IMAGE}" "${VM_NAME}"

log_ok "VM base '${VM_NAME}' creada exitosamente."
log_info "Próximo paso: ejecutar ./snapshot-macos-clean.sh para crear el golden snapshot."
