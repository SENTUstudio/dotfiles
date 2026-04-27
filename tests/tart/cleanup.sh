#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Cleanup Tart Test VMs
# =============================================================================
# Task: 4.6 — Destruye las VMs de prueba preservando `dotfiles-macos-base`
#       y su snapshot `dotfiles-macos-clean`.
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

VM_BASE="dotfiles-macos-base"
VM_CLEAN="dotfiles-macos-clean"

log_info() { echo -e "\033[1;34m[INFO]\033[0m  $*"; }
log_ok()   { echo -e "\033[1;32m[OK]\033[0m    $*"; }
log_warn() { echo -e "\033[1;33m[WARN]\033[0m  $*"; }
log_err()  { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; }

# --- Pre-flight checks -------------------------------------------------------

if ! command -v tart &>/dev/null; then
    log_err "Tart no está instalado. No hay nada que limpiar."
    exit 1
fi

# --- Identify VMs to delete --------------------------------------------------

mapfile -t all_vms < <(tart list | tail -n +2 | awk '{print $1}' || true)

delete_count=0
skip_count=0

for vm in "${all_vms[@]}"; do
    # Preservar VMs base y clean
    if [[ "${vm}" == "${VM_BASE}" || "${vm}" == "${VM_CLEAN}" ]]; then
        log_info "Preservando VM protegida: ${vm}"
        ((skip_count++)) || true
        continue
    fi

    # Solo eliminar VMs que parecen de test (patrones conocidos)
    if [[ "${vm}" == dotfiles-*-test-* || "${vm}" == dotfiles-fedora-test-* ]]; then
        log_info "Eliminando VM de prueba: ${vm}"
        tart delete "${vm}" && ((delete_count++)) || log_warn "No se pudo eliminar ${vm}"
    else
        log_warn "VM desconocida no eliminada (usa tart delete manualmente): ${vm}"
        ((skip_count++)) || true
    fi
done

log_ok "========================================"
log_ok "  Limpieza completada"
log_ok "  Eliminadas: ${delete_count}"
log_ok "  Preservadas: ${skip_count}"
log_ok "========================================"
