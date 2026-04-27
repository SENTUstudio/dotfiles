#!/usr/bin/env bash
# update-github-metadata.sh
# Actualiza descripción y topics del repo para SEO
# Uso: ./update-github-metadata.sh

set -euo pipefail

REPO="SENTUstudio/dotfiles"

# Descripción optimizada para SEO (máx 350 chars)
DESCRIPTION="Dotfiles installer with interactive TUI for Fedora, Arch, Debian, Ubuntu & macOS. Automated post-install via Ansible. 100+ apps: Neovim, Tmux, Docker, Zsh, Homebrew. One-command setup: curl | python3"

# Topics ordenados por prioridad (máx 20)
TOPICS=(
  dotfiles
  ansible
  fedora
  archlinux
  debian
  ubuntu
  macos
  homebrew
  neovim
  tmux
  zsh
  docker
  python
  shell
  cli
  tui
  setup-script
  post-install
  automation
  linux
)

echo "🔄 Actualizando metadata de ${REPO}..."

# Actualizar descripción
echo "📝 Descripción: ${DESCRIPTION}"
gh repo edit "${REPO}" --description "${DESCRIPTION}"

# Reemplazar topics (PUT reemplaza todos los existentes)
echo "🏷️  Topics: ${TOPICS[*]}"
JSON_TOPICS=$(printf '%s\n' "${TOPICS[@]}" | jq -R . | jq -s .)
gh api "repos/${REPO}/topics" \
  --method PUT \
  --input - <<< "{\"names\":${JSON_TOPICS}}" \
  --jq '.names | join(", ")'

echo "✅ Metadata actualizada exitosamente"
echo ""
echo "📋 Verificar en: https://github.com/${REPO}"
echo "🎯 Próximo paso: Subir social preview image (1200x630) en Settings > Social preview"
