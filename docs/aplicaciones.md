# Inventario de Aplicaciones — dotfiles

> Documento generado automáticamente a partir del análisis de variables Ansible.
> Fecha: 2025-04-27
> Rama base: `develop` (a7c8668)

---

## Tabla de Contenidos

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Runtimes y Gestores de Paquetes](#2-runtimes-y-gestores-de-paquetes)
3. [Dependencias Core](#3-dependencias-core)
4. [Dependencias Extendidas](#4-dependencias-extendidas)
5. [Post-Install Scripts](#5-post-install-scripts)
6. [Flatpak Apps](#6-flatpak-apps)
7. [Docker](#7-docker)
8. [Dotfiles Gestionados](#8-dotfiles-gestionados)
9. [Matriz de Compatibilidad Multi-Distro](#9-matriz-de-compatibilidad-multi-distro)
10. [Notas para macOS](#10-notas-para-macos)

---

## 1. Resumen Ejecutivo

Este proyecto instala aproximadamente **100+ paquetes y aplicaciones** divididos en:

| Categoría                      | Cantidad |
| ------------------------------ | -------- |
| Runtimes y gestores            | 9        |
| Dependencias Core              | ~25      |
| Dependencias Extendidas        | ~52      |
| Post-install scripts           | 7        |
| Herramientas adicionales       | 2        |
| Flatpak GUI apps               | 3        |
| Configuraciones dotfiles       | 18       |

Las variables por distro se encuentran en `ansible/vars/{Archlinux,Debian,RedHat}.yaml`.

---

## 2. Runtimes y Gestores de Paquetes

Estos siempre se instalan independientemente de la distro.

| Herramienta           | Método de Instalación                           | Propósito                      |
| --------------------- | ----------------------------------------------- | ------------------------------ |
| **Git**               | Gestor de paquetes nativo                       | Control de versiones           |
| **Python 3**          | Gestor de paquetes nativo                       | Runtime Python                 |
| **Go**                | Gestor de paquetes nativo                       | Compilar lazygit, d2           |
| **Rust / Cargo**      | Gestor de paquetes nativo                       | Compilar dust                  |
| **Ruby**              | Gestor de paquetes nativo                       | Tmuxinator (gem)               |
| **Node.js (via NVM)** | Script curl                                     | Última LTS                     |
| **Java (JDK)**        | Gestor de paquetes nativo                       | OpenJDK                        |
| **UV**                | Script curl (`https://astral.sh/uv/install.sh`) | Gestor Python moderno (Astral) |
| **Rye**               | Script curl (`https://rye.astral.sh/get`)       | Gestor Python (Astral)         |

**Archivos fuente:**
- `ansible/vars/global.yaml`
- `ansible/roles/04_install_uv/tasks/main.yml`
- `ansible/roles/05_install_nvm/tasks/main.yml`

---

## 3. Dependencias Core

Paquetes esenciales instalados en todas las distribuciones.

| Paquete                          | Fedora (dnf) | Archlinux (pacman) | Debian (apt) | macOS (brew)          | Notas               |
| -------------------------------- | ------------ | ------------------ | ------------ | --------------------- | ------------------- |
| git                              | ✅            | ✅                  | ✅            | ✅                     |                     |
| curl                             | ✅            | ✅                  | ✅            | ✅                     |                     |
| wget                             | ✅            | ✅                  | ✅            | ✅                     |                     |
| gcc                              | ✅            | ✅                  | ✅            | ✅ (CLI tools)         |                     |
| make                             | ✅            | ✅                  | ✅            | ✅ (CLI tools)         |                     |
| unzip                            | ✅            | ✅                  | ✅            | ✅                     |                     |
| zsh                              | ✅            | ✅                  | ✅            | ✅                     |                     |
| cargo                            | ✅            | ✅                  | ✅            | ✅                     |                     |
| g++                              | ✅            | —                  | ✅            | —                     | No aplica Arch      |
| python3                          | ✅            | python             | ✅            | ✅                     | Nombre varía        |
| ruby                             | ✅            | ✅                  | ✅            | ✅                     |                     |
| unrar                            | ✅            | ✅                  | ✅            | ❓                     |                     |
| p7zip                            | ✅            | ✅                  | ✅            | ❓                     |                     |
| p7zip-plugins                    | ✅            | —                  | ✅            | —                     | Solo Fedora/Debian  |
| xdg-user-dirs                    | ✅            | ✅                  | ✅            | ❌                     | Linux-only          |
| lsd                              | ✅            | ✅                  | ✅            | ✅                     |                     |
| java                             | ✅            | jdk-openjdk        | ✅            | ✅                     |                     |
| dnf-utils / apt-utils            | ✅            | —                  | ✅            | —                     | Utils gestor nativo |
| flatpak                          | ✅            | ✅                  | ✅            | ❌                     | Linux-only          |
| kernel-devel / linux-headers     | ✅            | ✅                  | ✅            | ❌                     | Linux-only          |
| automake                         | ✅            | ✅                  | ✅            | ✅                     |                     |
| perl                             | ✅            | ✅                  | ✅            | ✅                     |                     |
| elfutils-libelf-devel / elfutils | ✅            | ✅                  | ✅            | —                     | Linux-only          |
| fontconfig                       | ✅            | ✅                  | ✅            | ✅ (incluido en macOS) |                     |
| btop                             | ✅            | ✅                  | ✅            | ✅                     |                     |

**Archivos fuente:**
- `ansible/vars/RedHat.yaml` (Fedora)
- `ansible/vars/Archlinux.yaml`
- `ansible/vars/Debian.yaml`

---

## 4. Dependencias Extendidas

Aplicaciones y herramientas adicionales por categoría.

### 4.1 Desarrollo y Productividad

| Paquete      | Fedora         | Archlinux | Debian | macOS | Notas                        |
| ------------ | -------------- | --------- | ------ | ----- | ---------------------------- |
| lazygit      | ❌ (go install) | ✅         | ✅      | ✅     | Git TUI                      |
| ripgrep      | ✅              | ✅         | ✅      | ✅     | Búsqueda texto               |
| fd-find / fd | ✅              | ✅         | ✅      | ✅     | Búsqueda archivos            |
| neovim       | ✅              | ✅         | ✅      | ✅     | Editor                       |
| bat          | ✅              | ✅         | ✅      | ✅     | Cat mejorado                 |
| fzf          | ✅              | ✅         | ✅      | ✅     | Fuzzy finder                 |
| httpie       | ✅              | ✅         | ✅      | ✅     | HTTP client                  |
| zoxide       | ✅              | ✅         | ✅      | ✅     | Navegación directorios       |
| zeal         | ✅              | ✅         | ✅      | ❌     | Docs offline (Dash en macOS) |
| asciiquarium | ✅              | ✅         | ✅      | ❓     | Eye-candy terminal           |
| **opencode** | script curl     | script curl| script curl| ✅ brew | AI coding agent (OpenCode)   |

### 4.2 Terminales y Multiplexores

| Paquete    | Fedora | Archlinux | Debian | macOS   | Notas                            |
| ---------- | ------ | --------- | ------ | ------- | -------------------------------- |
| kitty      | ✅      | ✅         | ✅      | ✅       | Terminal                         |
| alacritty  | ✅      | ✅         | ✅      | ✅       | Terminal                         |
| **ghostty**| ✅ COPR| ✅         | ✅      | ✅ cask  | Terminal moderna (Zig + GPU)     |
| tmux       | ✅      | ✅         | ✅      | ✅       | Multiplexor                      |
| tmuxinator | ✅      | ✅         | ✅      | ✅ (gem) | Sesiones tmux                    |

### 4.3 Sistema y Monitoreo

| Paquete                      | Fedora | Archlinux | Debian | macOS       | Notas            |
| ---------------------------- | ------ | --------- | ------ | ----------- | ---------------- |
| fastfetch                    | ✅      | ✅         | ✅      | ✅           | Info sistema     |
| htop                         | ✅      | ✅         | ✅      | ✅           | Procesos         |
| bpytop                       | ✅      | ✅         | ✅      | ✅           | Monitor recursos |
| lm_sensors                   | ✅      | ✅         | ✅      | ❌           | Linux-only       |
| proselint                    | ✅      | —         | ✅      | ❓           | Linter prosa     |
| util-linux-user / util-linux | ✅      | ✅         | ✅      | ❌           | Linux-only       |
| anacron / cron               | ✅      | ✅         | ✅      | ❌ (launchd) | Scheduling       |

### 4.4 Lua y Soporte Neovim

| Paquete                        | Fedora | Archlinux | Debian | macOS | Notas                    |
| ------------------------------ | ------ | --------- | ------ | ----- | ------------------------ |
| lua-devel / lua                | ✅      | ✅         | ✅      | ✅     |                          |
| luarocks                       | ✅      | ✅         | ✅      | ✅     | Paquetes Lua             |
| python3-neovim / python-neovim | ✅      | ✅         | ✅      | ✅     | Soporte Python en Neovim |

### 4.5 Docker y Contenedores

| Paquete             | Fedora | Archlinux | Debian | macOS | Notas                        |
| ------------------- | ------ | --------- | ------ | ----- | ---------------------------- |
| docker-cli / docker | ✅      | ✅         | ✅      | ❌     | Docker Desktop cask en macOS |
| containerd          | ✅      | ✅         | ✅      | —     |                              |
| docker-compose      | ✅      | ✅         | ✅      | —     |                              |
| docker-switch       | —      | —         | ✅      | —     | Solo Debian                  |

### 4.6 Multimedia — Editores y Reproductores

| Paquete        | Fedora | Archlinux | Debian | macOS                | Notas              |
| -------------- | ------ | --------- | ------ | -------------------- | ------------------ |
| vlc            | ✅      | ✅         | ✅      | ✅ (cask)             | Reproductor        |
| mpv            | ✅      | ✅         | ✅      | ✅                    | Reproductor        |
| kdenlive       | ✅      | ✅         | ✅      | ❌ (cask alternativo) | Video editing      |
| openshot       | ✅      | ✅         | ✅      | ❌                    | Video editing      |
| flowblade      | ✅      | ✅         | ✅      | ❌                    | Video editing      |
| audacity       | ✅      | ✅         | ✅      | ✅ (cask)             | Audio editing      |
| muse           | ✅      | ✅         | ✅      | ❓                    | Secuenciador       |
| lmms           | ✅      | ✅         | ✅      | ❌ (cask)             | DAW                |
| amarok         | ✅      | —         | —      | ❌                    | Reproductor música |
| soundconverter | ✅      | ✅         | —      | ❌                    | Conversión audio   |
| gnome-mpv      | ✅      | —         | —      | ❌                    | Linux-only         |

### 4.7 Multimedia — Codecs y Librerías

| Paquete                                  | Fedora | Archlinux | Debian | macOS | Notas                  |
| ---------------------------------------- | ------ | --------- | ------ | ----- | ---------------------- |
| ffmpeg                                   | ✅      | ✅         | ✅      | ✅     | Conversión video/audio |
| gstreamer1-* / gstreamer + gst-plugins-* | ✅      | ✅         | ✅      | ❌     | Framework multimedia   |
| xine-lib + extras                        | ✅      | ✅         | ✅      | ❌     | Reproductor libs       |
| libdvdread                               | ✅      | ✅         | ✅      | ❌     | DVD libs               |
| libdvdnav                                | ✅      | ✅         | ✅      | ❌     | DVD navegación         |
| lsdvd                                    | ✅      | ✅         | ✅      | ❌     | DVD info               |
| libdvbpsi                                | ✅      | ✅         | ✅      | ❌     | DVB                    |
| libmatroska                              | ✅      | ✅         | ✅      | ❌     | MKV                    |
| xvidcore                                 | ✅      | ✅         | ✅      | ❌     | Codecs                 |

### 4.8 Gráficos y Oficina

| Paquete                 | Fedora | Archlinux            | Debian | macOS    | Notas            |
| ----------------------- | ------ | -------------------- | ------ | -------- | ---------------- |
| gimp                    | ✅      | ✅                    | ✅      | ✅ (cask) | Imágenes         |
| inkscape                | ✅      | ✅                    | ✅      | ✅ (cask) | Vector           |
| libreoffice-writer      | ✅      | libreoffice-fresh    | ✅      | ✅ (cask) | Oficina          |
| libreoffice-calc        | ✅      | libreoffice-fresh    | ✅      | ✅ (cask) | Hojas de cálculo |
| libreoffice-impress     | ✅      | libreoffice-fresh    | ✅      | ✅ (cask) | Presentaciones   |
| libreoffice-draw        | ✅      | libreoffice-fresh    | ✅      | ✅ (cask) | Dibujo           |
| libreoffice-langpack-es | ✅      | libreoffice-fresh-es | ✅      | ✅        | Español          |

### 4.9 Comunicación y Conectividad

| Paquete     | Fedora | Archlinux | Debian | macOS    | Notas                   |
| ----------- | ------ | --------- | ------ | -------- | ----------------------- |
| discord     | ✅      | ✅         | ✅      | ✅ (cask) | Chat                    |
| kde-connect | ✅      | ✅         | ✅      | ❌        | Integración móvil (KDE) |

### 4.10 Virtualización

| Paquete      | Fedora | Archlinux | Debian | macOS | Notas              |
| ------------ | ------ | --------- | ------ | ----- | ------------------ |
| virt-manager | ✅      | ✅         | ✅      | ❌     | VMs (UTM en macOS) |
| qemu         | ✅      | ✅         | ✅      | ❌     | Emulación          |

---

## 5. Post-Install Scripts

Comandos ejecutados después de la instalación de paquetes.

| Comando                                                             | Descripción             | Condicional                  |
| ------------------------------------------------------------------- | ----------------------- | ---------------------------- |
| `go install oss.terrastruct.com/d2@latest`                          | Diagramas as-code       | `install_d2: true`           |
| `curl -fsS https://dl.brave.com/install.sh                          | sh`                     | Navegador Brave              | `install_brave: true` |
| `git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm` | Tmux Plugin Manager     | `install_tmux_plugins: true` |
| `gem install tmuxinator`                                            | Gestor de sesiones tmux | `install_tmuxinator: true`   |
| `sudo usermod -aG docker $USER`                                     | Permisos Docker         | `setup_docker_user: true`    |
| `curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh       | sh`                     | Shell history sync           | `install_atuin: true` |
| `cargo install du-dust`                                             | Disco usage (dust)      | `install_dust: true`         |

**Archivo fuente:** `ansible/vars/post_install.yaml`, `ansible/roles/09_post_install/defaults/main.yml`

---

## 6. Flatpak Apps

Aplicaciones GUI instaladas via Flatpak (Linux-only).

| App                | ID Flatpak                       |
| ------------------ | -------------------------------- |
| **Obsidian**       | `md.obsidian.Obsidian`           |
| **Mission Center** | `io.missioncenter.MissionCenter` |
| **Bitwarden**      | `com.bitwarden.desktop`          |

**Archivo fuente:** `ansible/vars/flatpak.yaml`

---

## 7. Docker

Role dedicado (`08_install_docker`) que instala:
- Docker CE / docker-cli
- containerd
- docker-compose
- Configura grupo `docker`
- Configura systemd para arranque automático

**Nota macOS:** Requiere Docker Desktop (instalable via `homebrew_cask`).

**Archivos fuente:**
- `ansible/roles/08_install_docker/tasks/main.yml`
- `ansible/roles/08_install_docker/defaults/main.yml`

---

## 8. Dotfiles Gestionados

Configuraciones personales copiadas a `~/.config/` y `~/`.

| Tool                | Ruta Destino              | Plataforma     |
| ------------------- | ------------------------- | -------------- |
| **Alacritty**       | `~/.config/alacritty`     | Cross-platform |
| **BSPWM**           | `~/.config/bspwm`         | Linux-only     |
| **Fastfetch**       | `~/.config/fastfetch`     | Cross-platform |
| **GitHub CLI (gh)** | `~/.config/gh`            | Cross-platform |
| **Git**             | `~/.config/git`           | Cross-platform |
| **Kitty**           | `~/.config/kitty`         | Cross-platform |
| **Lazygit**         | `~/.config/lazygit`       | Cross-platform |
| **MPD**             | `~/.config/mpd`           | Linux-only     |
| **NCMPCPP**         | `~/.config/ncmpcpp`       | Linux-only     |
| **Neovim**          | `~/.config/nvim`          | Cross-platform |
| **Oh My Posh**      | `~/.config/ohmyposh`      | Cross-platform |
| **Paru**            | `~/.config/paru`          | Arch-only      |
| **Ranger**          | `~/.config/ranger`        | Cross-platform |
| **Sentu**           | `~/.config/sentu`         | Cross-platform |
| **Tmux**            | `~/.config/tmux`          | Cross-platform |
| **Tmuxinator**      | `~/.config/tmuxinator`    | Cross-platform |
| **Zsh**             | `~/.zshrc`, `~/.p10k.zsh` | Cross-platform |

---

## 9. Matriz de Compatibilidad Multi-Distro

| Sistema            | Archivo Vars                  | Estado          | Gestor             |
| ------------------ | ----------------------------- | --------------- | ------------------ |
| **Fedora**         | `ansible/vars/RedHat.yaml`    | ✅ Probado       | dnf                |
| **Archlinux**      | `ansible/vars/Archlinux.yaml` | ✅ Probado       | pacman + yay (AUR) |
| **Debian/Ubuntu**  | `ansible/vars/Debian.yaml`    | ⚠️ Parcial       | apt-get            |
| **macOS**          | `ansible/vars/Darwin.yaml`    | 🔄 En desarrollo | homebrew           |
| **openSUSE**       | —                             | 📝 En roadmap    | zypper             |
| **Windows (WSL2)** | —                             | 📝 En roadmap    | apt/dnf            |

---

## 10. Notas para macOS

### 10.1 Paquetes con equivalente Homebrew
La mayoría de los paquetes core y muchos extended tienen equivalente en Homebrew:
- `fd-find` → `fd`
- `docker-cli` → `docker` (formula)
- `libreoffice-*` → `libreoffice` (cask)
- `discord` → `discord` (cask)

### 10.2 Paquetes a omitir en macOS
Estos paquetes no tienen sentido en macOS:

| Paquete                       | Razón                              |
| ----------------------------- | ---------------------------------- |
| xdg-user-dirs                 | Linux-only (XDG spec)              |
| flatpak                       | Linux-only package manager         |
| kernel-devel / linux-headers  | Linux kernel                       |
| lm_sensors                    | Hardware sensors Linux             |
| util-linux-user / util-linux  | Linux utilities                    |
| anacron / cron                | macOS usa launchd                  |
| kde-connect                   | Integración KDE/Linux              |
| kdenlive, openshot, flowblade | Editores video (alternativas cask) |
| gstreamer1-*                  | Framework multimedia Linux         |
| xine-lib, libdvdread, etc.    | Librerías multimedia Linux         |
| virt-manager, qemu            | Virtualización (UTM en macOS)      |
| libmatroska, xvidcore         | Codecs Linux                       |

### 10.3 Apps que requieren Homebrew Cask
Algunas aplicaciones en macOS se instalan mejor como cask:

| App            | Tipo | Equivalencia Linux      |
| -------------- | ---- | ----------------------- |
| Docker Desktop | cask | docker-cli + containerd |
| Brave          | cask | script curl             |
| Discord        | cask | discord (dnf/pacman)    |
| Obsidian       | cask | flatpak                 |
| Bitwarden      | cask | flatpak                 |
| LibreOffice    | cask | libreoffice-*           |
| GIMP           | cask | gimp                    |
| Inkscape       | cask | inkscape                |
| VLC            | cask | vlc                     |
| Audacity       | cask | audacity                |
| LMMS           | cask | lmms                    |
| **Ghostty**    | cask | ghostty (COPR/pacman)   |
| **OpenCode**   | brew | script curl             |

### 10.4 Post-Install en macOS
Algunos comandos de post-install no aplican:

| Comando                                    | macOS                                        |
| ------------------------------------------ | -------------------------------------------- |
| `sudo usermod -aG docker $USER`            | ❌ No aplica (Docker Desktop maneja permisos) |
| `curl -fsS https://dl.brave.com/install.sh | sh`                                          | ⚠️ Mejor usar `brew install --cask brave-browser` |
| `cargo install du-dust`                    | ✅ Funciona                                   |
| `go install ...`                           | ✅ Funciona                                   |

### 10.5 Ghostty — Instalación Detallada

Ghostty es un emulador de terminal moderno escrito en Zig con aceleración GPU.

| Plataforma | Método | Comando |
|------------|--------|---------|
| **macOS** | Homebrew Cask | `brew install --cask ghostty` |
| **Fedora** | COPR | `dnf copr enable scottames/ghostty && dnf install ghostty` |
| **Archlinux** | Repos oficiales | `pacman -S ghostty` |
| **Debian/Ubuntu** | **Snap** | `snap install ghostty --classic` |

**Nota:** En Fedora también disponible via Terra: `dnf install ghostty`

### 10.6 OpenCode — Instalación Detallada

OpenCode es un agente de IA open source para coding.

| Plataforma | Método | Comando |
|------------|--------|---------|
| **Universal** | Script | `curl -fsSL https://opencode.ai/install \| bash` |
| **macOS** | Homebrew | `brew install opencode` |
| **macOS Desktop** | Homebrew Cask | `brew install opencode-desktop` |
| **npm** | npm | `npm install -g opencode` |

**Nota:** Para dotfiles, se recomienda el script curl (multi-plataforma) o brew en macOS.

---

## Referencias

- `ansible/vars/global.yaml` — Scripts UV y Rye
- `ansible/vars/RedHat.yaml` — Variables Fedora
- `ansible/vars/Archlinux.yaml` — Variables Archlinux
- `ansible/vars/Debian.yaml` — Variables Debian/Ubuntu
- `ansible/vars/post_install.yaml` — Comandos post-install
- `ansible/vars/flatpak.yaml` — Apps Flatpak
- `ansible/roles/08_install_docker/defaults/main.yml` — Config Docker
- `ansible/roles/09_post_install/defaults/main.yml` — Flags condicionales
- [Ghostty Install Docs](https://ghostty.org/docs/install/binary) — Instalación oficial de Ghostty
- [OpenCode Install](https://opencode.ai) — Instalación oficial de OpenCode

---

*Documento generado durante el desarrollo de feature/mac-install. Mantener actualizado al agregar/quitar paquetes.*
