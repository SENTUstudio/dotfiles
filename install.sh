#!/usr/bin/env bash
#
# SENTU Dotfiles Installer
# Bootstrap script that installs sentu-dotfiles manager and deploys dotfiles
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/SENTUstudio/dotfiles/main/install.sh | bash
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/SENTUstudio/dotfiles.git"
GITHUB_API="https://api.github.com/repos/SENTUstudio/dotfiles/releases/latest"
DOTFILES_DIR="$HOME/dotfiles"
INSTALL_DIR="$HOME/.local/bin"
BINARY_NAME="sentu-dotfiles"
REPO_BRANCH="main"

# Logging functions
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS and architecture
detect_platform() {
    local os arch

    os=$(uname -s | tr '[:upper:]' '[:lower:]')
    arch=$(uname -m)

    case "$os" in
        linux)
            os="linux"
            ;;
        darwin)
            os="darwin"
            ;;
        *)
            error "Sistema operativo no soportado: $os"
            exit 1
            ;;
    esac

    case "$arch" in
        x86_64)
            arch="amd64"
            ;;
        arm64|aarch64)
            arch="arm64"
            ;;
        *)
            error "Arquitectura no soportada: $arch"
            exit 1
            ;;
    esac

    echo "${os}_${arch}"
}

# Ensure ~/.local/bin exists and is in PATH
ensure_install_dir() {
    if [[ ! -d "$INSTALL_DIR" ]]; then
        info "Creando directorio $INSTALL_DIR..."
        mkdir -p "$INSTALL_DIR"
    fi

    # Check if in PATH
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        warn "$INSTALL_DIR no está en tu PATH"
        info "Agregando $INSTALL_DIR al PATH..."

        # Detect shell
        local shell_rc
        if [[ -n "${ZSH_VERSION:-}" ]] || [[ "$SHELL" == */zsh ]]; then
            shell_rc="$HOME/.zshrc"
        else
            shell_rc="$HOME/.bashrc"
        fi

        if ! grep -qxF "export PATH=\"$INSTALL_DIR:\$PATH\"" "$shell_rc" 2>/dev/null; then
            echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$shell_rc"
        fi
        success "PATH actualizado en $shell_rc"
        info "Ejecutá 'source $shell_rc' o reiniciá tu terminal después de la instalación"
    fi
}

# Try to download latest release binary from GitHub
download_release_binary() {
    local platform="$1"
    local os=${platform%_*}
    local arch=${platform#*_}
    local binary_file="sentu-dotfiles_${os}_${arch}"
    local download_url

    info "Buscando última release en GitHub..."

    # Get latest release download URL
    download_url=$(curl -fsSL "$GITHUB_API" 2>/dev/null | \
        grep -o '"browser_download_url": *"[^"]*' | \
        grep "$binary_file" | \
        head -1 | \
        sed 's/.*": *"//')

    if [[ -z "$download_url" ]]; then
        warn "No se encontró un binario precompilado para $platform"
        return 1
    fi

    info "Descargando sentu-dotfiles desde GitHub Releases..."
    info "URL: $download_url"

    if curl -fsSL "$download_url" -o "$INSTALL_DIR/$BINARY_NAME"; then
        chmod +x "$INSTALL_DIR/$BINARY_NAME"
        success "sentu-dotfiles descargado e instalado desde GitHub Releases"
        return 0
    else
        warn "Error descargando el binario"
        return 1
    fi
}

# Clone or update the dotfiles repository
clone_or_update_repo() {
    if [[ -d "$DOTFILES_DIR/.git" ]]; then
        info "Actualizando repositorio existente en $DOTFILES_DIR..."
        cd "$DOTFILES_DIR"
        git fetch origin
        if [[ -n $(git status --porcelain) ]]; then
            warn "Se detectaron cambios locales en $DOTFILES_DIR."
            info "Guardando cambios locales en stash..."
            git stash push -m "auto-stash before update"
        fi
        git reset --hard "origin/$REPO_BRANCH"
        success "Repositorio actualizado"
    else
        if [[ -d "$DOTFILES_DIR" ]]; then
            warn "$DOTFILES_DIR existe pero no es un repositorio git."
            local backup_name="${DOTFILES_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
            info "Renombrando a $backup_name..."
            mv "$DOTFILES_DIR" "$backup_name"
        fi
        info "Clonando repositorio de dotfiles..."
        git clone -b "$REPO_BRANCH" "$REPO_URL" "$DOTFILES_DIR"
        success "Repositorio clonado"
    fi
}

# Install Go if not present
install_go_if_needed() {
    if command -v go &>/dev/null; then
        local go_version
        go_version=$(go version | awk '{print $3}' | sed 's/go//')
        info "Go encontrado: $go_version"
        return 0
    fi

    warn "Go no está instalado. Es necesario para compilar sentu-dotfiles."
    info "Instalando Go..."

    local platform go_version="1.23.4"
    platform=$(detect_platform)

    local os=${platform%_*}
    local arch=${platform#*_}

    local go_tarball="go${go_version}.${os}-${arch}.tar.gz"
    local go_url="https://go.dev/dl/${go_tarball}"

    cd /tmp
    curl -fsSL "$go_url" -o "$go_tarball"
    sudo rm -rf /usr/local/go
    sudo tar -C /usr/local -xzf "$go_tarball"
    rm -f "$go_tarball"

    export PATH="/usr/local/go/bin:$PATH"

    if command -v go &>/dev/null; then
        success "Go instalado correctamente"
    else
        error "No se pudo instalar Go. Instalalo manualmente desde https://go.dev/dl/"
        exit 1
    fi
}

# Build sentu-dotfiles from source
build_from_source() {
    info "Compilando sentu-dotfiles desde el repositorio..."
    cd "$DOTFILES_DIR"

    if ! command -v go &>/dev/null; then
        export PATH="/usr/local/go/bin:$PATH"
    fi

    go build -ldflags="-s -w" -o "$INSTALL_DIR/$BINARY_NAME" ./cmd/sentu-dotfiles
    chmod +x "$INSTALL_DIR/$BINARY_NAME"
    success "sentu-dotfiles compilado e instalado en $INSTALL_DIR/$BINARY_NAME"
}

# Main installation flow
main() {
    echo -e "${GREEN}"
    echo "  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤ Ingeniería de Datos & Data Science ├┒"
    echo "  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤  Dotfiles Installer                 ├┚"
    echo "                .studio"
    echo -e "${NC}"

    local platform
    platform=$(detect_platform)
    info "Plataforma detectada: $platform"

    ensure_install_dir

    # Clone or update the dotfiles repository (always needed)
    clone_or_update_repo

    # Strategy 1: Try to download pre-compiled binary from GitHub Releases
    if download_release_binary "$platform"; then
        info "Usando binario precompilado de GitHub Releases"
    else
        warn "No se pudo descargar el binario. Usando fallback de compilación..."

        # Strategy 2: Fallback to building from source
        install_go_if_needed
        build_from_source
    fi

    # Ensure binary is in current PATH for this session
    export PATH="$INSTALL_DIR:$PATH"

    success "sentu-dotfiles está listo para usar"
    echo ""
    info "Ejecutando sentu-dotfiles..."
    echo ""

    # Run the manager
    exec "$INSTALL_DIR/$BINARY_NAME" "$@"
}

# Run main
main "$@"
