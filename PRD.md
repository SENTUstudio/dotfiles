# Product Requirements Document (PRD)

## dotfiles — SENTUstudio

**Versión:** 1.0.0  
**Fecha:** 2025-04-27  
**Autor:** SENTUstudio  
**Estado:** Activo / En desarrollo  

---

## 1. Resumen Ejecutivo

`dotfiles` es el sistema de post-instalación automatizado de SENTUstudio. Su propósito es transformar un sistema operativo recién instalado (principalmente Fedora KDE) en un entorno de desarrollo productivo y personalizado en cuestión de minutos, sin intervención manual más allá de la contraseña de sudo.

El proyecto consta de dos componentes principales:

1. **`sentu_install.py`** — Script bootstrapper escrito en Python 3 que descarga, prepara y lanza el motor de orquestación.
2. **Motor Ansible** — Playbook y roles que instalan paquetes, repositorios, fuentes, dependencias de desarrollo y despliegan archivos de configuración personalizados.

---

## 2. Objetivos del Producto

| ID | Objetivo | Prioridad |
|----|----------|-----------|
| OBJ-1 | Reducir el tiempo de configuración de un sistema nuevo de horas a minutos | Alta |
| OBJ-2 | Garantizar reproducibilidad: el mismo playbook produce el mismo entorno siempre | Alta |
| OBJ-3 | Centralizar y versionar todas las configuraciones personales (dotfiles) | Alta |
| OBJ-4 | Soportar múltiples sistemas operativos (Linux multi-distro, macOS, Windows) | Media |
| OBJ-5 | Minimizar la curva de aprendizaje para nuevos usuarios del proyecto | Media |

---

## 3. Alcance

### 3.1 Dentro del alcance (In Scope)

- Instalación automática de dependencias mínimas (`git`, `python3`, `ansible`).
- Clonación del repositorio `dotfiles` desde GitHub.
- Ejecución de playbook Ansible con roles definidos.
- Instalación de repositorios de terceros (RPM Fusion, Docker, Google Chrome, Lazygit COPR).
- Instalación de paquetes core y extendidos vía gestor de paquetes nativo.
- Instalación de gestores de Python modernos (`uv`, `rye`).
- Instalación de fuentes tipográficas.
- Despliegue de archivos de configuración personales a `~/.config/` y `~/`.
- Comandos de post-instalación (Flatpak, Brave, Obsidian, Docker group, etc.).

### 3.2 Fuera del alcance (Out of Scope)

- Configuración de hardware específico (drivers de GPU, Wi-Fi, etc.).
- Backup o migración de datos de usuario.
- Configuración de red o VPN.
- Gestión de secretos o credenciales (tokens, claves SSH, etc.).
- Interfaz gráfica de usuario (GUI) para el instalador.

---

## 4. Público Objetivo

- **Usuario primario:** Desarrolladores de SENTUstudio que necesitan replicar su entorno de trabajo en nuevas máquinas o VMs.
- **Usuario secundario:** Cualquier persona que use Fedora KDE y quiera un entorno de desarrollo preconfigurado con herramientas modernas (Neovim, Tmux, Zsh, Kitty, etc.).
- **Usuario terciario (futuro):** Usuarios de otras distros Linux, macOS y Windows.

---

## 5. Requisitos Funcionales

### 5.1 Bootstrapper (`sentu_install.py`)

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| FR-1 | Detectar el sistema operativo (Linux, macOS, Windows) | Alta |
| FR-2 | Verificar e instalar `git` si no está presente (con soporte para `apt`, `dnf`, `pacman`, `yum`) | Alta |
| FR-3 | Clonar el repositorio `dotfiles` a `~/dotfiles`; permitir sobrescribir si ya existe | Alta |
| FR-4 | Verificar e instalar `ansible` si no está presente (vía `pip`) | Alta |
| FR-5 | Ejecutar el playbook `ansible/playbook.yml` con el inventario local | Alta |
| FR-6 | Mostrar mensajes de progreso con formato visual (logo ASCII + colores) | Media |
| FR-7 | Manejar errores de forma elegante, mostrando mensajes claros al usuario | Alta |

### 5.2 Motor Ansible

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| FR-8 | Leer configuración centralizada desde `vars/installer_config.yaml` | Alta |
| FR-9 | Ejecutar roles en orden determinista (test → base → repos → core → uv → rye → extended → post → fonts → dotfiles) | Alta |
| FR-10 | Instalar repositorios de terceros de forma idempotente | Alta |
| FR-11 | Instalar paquetes core y extendidos según la distro detectada | Alta |
| FR-12 | Instalar `uv` y `rye` desde scripts oficiales de Astral | Alta |
| FR-13 | Ejecutar comandos de post-instalación (scripts arbitrarios) | Media |
| FR-14 | Instalar fuentes tipográficas en el sistema | Media |
| FR-15 | Copiar archivos de `config/` a `~/.config/` y de `home/` a `~/` | Alta |
| FR-16 | Garantizar idempotencia: re-ejecutar el playbook no debe romper nada | Alta |

### 5.3 Configuraciones Gestionadas (Dotfiles)

Las siguientes herramientas tienen sus configuraciones versionadas en el repositorio:

- **Terminales:** Alacritty, Kitty
- **Shell:** Zsh (con Oh My Posh / Powerlevel10k)
- **Editor:** Neovim
- **Multiplexor:** Tmux (con Tmuxinator)
- **Gestor de archivos:** Ranger
- **WM:** BSPWM
- **Info de sistema:** Fastfetch
- **CLI tools:** Lazygit, GH (GitHub CLI)
- **Media:** MPD, NCMPCPP
- **AUR Helper:** Paru
- **Personalizado:** Sentu config

---

## 6. Requisitos No Funcionales

| ID | Requisito | Métrica / Criterio |
|----|-----------|-------------------|
| NFR-1 | **Tiempo de ejecución** total del instalador en una conexión decente | < 15 minutos |
| NFR-2 | **Idempotencia** del playbook Ansible | Ejecuciones consecutivas sin errores y sin cambios innecesarios |
| NFR-3 | **Compatibilidad** mínima | Fedora KDE 41+ (actual); diseñado para extensión futura |
| NFR-4 | **Mantenibilidad** del código | Estructura modular por roles; variables centralizadas en `vars/` |
| NFR-5 | **Claridad de logs** | Salida verbose (`-v`) de Ansible; mensajes coloreados del bootstrapper |
| NFR-6 | **Seguridad** | Uso de `sudo` solo donde es necesario; sin hardcodeo de credenciales |

---

## 7. Arquitectura y Componentes

### 7.1 Diagrama de Componentes (Resumen)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Usuario / Sistema Nuevo                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │ curl | python3
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Bootstrapper: sentu_install.py                                  │
│  ├── Detecta OS                                                  │
│  ├── Instala Git (si falta)                                      │
│  ├── Clona repo dotfiles → ~/dotfiles                            │
│  ├── Instala Ansible (si falta)                                  │
│  └── Ejecuta ansible-playbook                                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Motor Ansible                                                   │
│  ├── vars/installer_config.yaml  (config centralizada)           │
│  ├── playbook.yml                (orquestador)                   │
│  └── roles/                                                      │
│       ├── test/                                                  │
│       ├── base_system_configuration/                             │
│       ├── add_repositories/                                      │
│       ├── install_core_dependencies/                             │
│       ├── install_uv/                                            │
│       ├── install_rye/                                           │
│       ├── install_extended_dependencies/                         │
│       ├── install_post_install/                                  │
│       ├── install_fonts/                                         │
│       └── dotfiles_management/                                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ despliega
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Destino                                                         │
│  ├── ~/.config/  ← config/ (alacritty, nvim, tmux, etc.)        │
│  └── ~/          ← home/ (.zshrc, .p10k.zsh, etc.)              │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Estructura de Archivos

```
dotfiles/
├── ansible/
│   ├── playbook.yml
│   ├── inventory.ini
│   ├── vars/
│   │   └── installer_config.yaml
│   └── roles/
│       ├── test/
│       ├── base_system_configuration/
│       ├── add_repositories/
│       ├── install_core_dependencies/
│       ├── install_uv/
│       ├── install_rye/
│       ├── install_extended_dependencies/
│       ├── install_post_install/
│       ├── install_fonts/
│       └── dotfiles_management/
├── config/
│   ├── alacritty/
│   ├── bspwm/
│   ├── fastfetch/
│   ├── gh/
│   ├── git/
│   ├── kitty/
│   ├── lazygit/
│   ├── mpd/
│   ├── ncmpcpp/
│   ├── nvim/
│   ├── ohmyposh/
│   ├── paru/
│   ├── ranger/
│   ├── sentu/
│   ├── tmux/
│   ├── tmuxinator/
│   └── zsh/
├── home/
│   ├── .p10k.zsh
│   └── .zshrc
├── sentu_install.py
└── README.md
```

---

## 8. Flujo de Instalación

1. **Inicio:** El usuario ejecuta el comando curl en su terminal.
2. **Bootstrap:** `sentu_install.py` se descarga y ejecuta.
3. **Detección:** Se detecta el SO y el gestor de paquetes disponible.
4. **Preparación:** Se instalan `git` y `ansible` si faltan.
5. **Clonación:** Se clona el repo `dotfiles` a `~/dotfiles`.
6. **Orquestación:** Se ejecuta `ansible-playbook` con `playbook.yml`.
7. **Secuencia de roles:** Cada role realiza su tarea en orden:
   - `test`: validaciones iniciales.
   - `base_system_configuration`: ajustes base del sistema.
   - `add_repositories`: agrega repositorios de terceros.
   - `install_core_dependencies`: instala paquetes esenciales.
   - `install_uv` / `install_rye`: gestores de Python modernos.
   - `install_extended_dependencies`: aplicaciones y herramientas adicionales.
   - `install_post_install`: comandos arbitrarios de post-instalación.
   - `install_fonts`: fuentes tipográficas.
   - `dotfiles_management`: copia archivos de configuración personales.
8. **Finalización:** El entorno está listo para usar.

---

## 9. Dependencias y Requisitos Técnicos

### 9.1 Sistemas Operativos Soportados

| SO | Versión | Estado |
|----|---------|--------|
| Fedora KDE | 41+ | ✅ Probado |
| OpenSUSE | Tumbleweed / Leap | 🔄 En roadmap |
| macOS | 14+ | 🔄 En roadmap |
| Windows | 11 (WSL2) | 🔄 En roadmap |
| Ubuntu / Debian | 24.04+ | 🔄 En roadmap |
| Arch Linux | Rolling | 🔄 En roadmap |

### 9.2 Dependencias del Bootstrapper

- `python3` (3.10+)
- Acceso a internet
- `curl` o `wget` para la descarga inicial

### 9.3 Dependencias Instaladas por el Proyecto

**Core:**
`git`, `curl`, `wget`, `gcc`, `make`, `unzip`, `zsh`, `golang`, `cargo`, `g++`, `python3`, `ruby`, `lsd`, `java`, `flatpak`, `kernel-devel`, `automake`, `perl`, `elfutils-libelf-devel`

**Extended:**
`lazygit`, `ripgrep`, `fd-find`, `neovim`, `fastfetch`, `zoxide`, `kitty`, `lua-devel`, `luarocks`, `docker-ce`, `bat`, `fzf`, `httpie`, `tmux`, `htop`, `discord`, `alacritty`, `kdenlive`, `openshot`, `vlc`, `mpv`, `audacity`, `gimp`, `inkscape`, `libreoffice-*`, `virt-manager`, `qemu`

**Post-install:**
`d2`, `brave`, `tpm` (tmux plugin manager), `tmuxinator`, `obsidian` (flatpak), `atuin`, `du-dust`

---

## 10. Roadmap y Futuras Mejoras

| Fase | Feature | Prioridad | Estimación |
|------|---------|-----------|------------|
| v1.1 | Soporte para OpenSUSE (detección de `zypper`) | Alta | 1 sprint |
| v1.2 | Soporte para Arch Linux (`pacman`) | Alta | 1 sprint |
| v1.3 | Soporte para macOS (`brew`) | Media | 2 sprints |
| v1.4 | Soporte para Ubuntu/Debian (`apt`) | Media | 1 sprint |
| v1.5 | Windows WSL2 | Baja | 2 sprints |
| v2.0 | Configuración por perfiles (minimal, full, data-science) | Media | 2 sprints |
| v2.1 | Encriptación de secretos (Ansible Vault) | Baja | 1 sprint |
| v2.2 | Tests automáticos con Molecule | Media | 2 sprints |
| v2.3 | Interfaz TUI (Text User Interface) con Rich/Blessed | Baja | 3 sprints |

---

## 11. Métricas de Éxito

- **Adopción interna:** 100% de nuevas máquinas de SENTUstudio configuran con este proyecto.
- **Tiempo de setup:** Reducción del 90% vs. configuración manual.
- **Estabilidad:** 0 errores críticos en ejecuciones consecutivas sobre Fedora 41+.
- **Contribuciones externas:** Al menos 5 forks o PRs de la comunidad en el primer año.

---

## 12. Riesgos y Mitigaciones

| Riesgo | Impacto | Probabilidad | Mitigación |
|--------|---------|--------------|------------|
| Cambio en repos de terceros (RPM Fusion, Docker) rompe la instalación | Alto | Media | Monitoreo periódico; variables externalizadas en `installer_config.yaml` |
| Ansible no disponible en sistema mínimo | Medio | Baja | El bootstrapper instala `ansible` vía `pip` automáticamente |
| Conflicto de paquetes entre versiones de Fedora | Medio | Media | Uso de `--allowerasing` en `dnf`; testing en VM antes de release |
| Divergencia entre configuraciones locales y el repo | Alto | Alta | Política de "el repo es la fuente de verdad"; sincronización periódica |

---

## 13. Glosario

| Término | Definición |
|---------|------------|
| **Dotfiles** | Archivos de configuración de usuario que comienzan con `.` (ej: `.bashrc`, `.vimrc`). |
| **Bootstrapper** | Script inicial que prepara el entorno para ejecutar el sistema principal. |
| **Playbook** | Archivo YAML de Ansible que define la orquestación de tareas y roles. |
| **Role** | Estructura reutilizable en Ansible que agrupa tareas, variables y templates. |
| **Idempotencia** | Propiedad de una operación que puede aplicarse múltiples veces sin cambiar el resultado más allá de la primera aplicación. |
| **COPR** | Repositorio personal de Fedora (Cool Other Package Repo), similar a PPA en Ubuntu. |
| **Flatpak** | Sistema de distribución de aplicaciones sandboxed para Linux. |

---

## 14. Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0.0 | 2025-04-27 | SENTUstudio | Documento inicial basado en la exploración del repositorio. |

---

*Documento generado automáticamente a partir de la exploración del código fuente. Mantener sincronizado con cambios en la arquitectura y funcionalidades.*
