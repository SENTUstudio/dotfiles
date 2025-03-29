```
█▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤ DATA ENGINEER                                       ├┒
▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤ Obteniendo datos para empresas, personas... para ti ├┚
                STUDIO
```

# dotfiles

Proyecto que se encarga de hacer una post-instalación a un sistema operativo resién instalado, donde instala las aplicaciones bases de mi preferencia y copia mis archivos de configuración al nuevo sistema. consta de un script llamado sentu_install.py que se usa por medio de curl para llamar a todo el proyecto en formato zip desde un repositorio, lo extrae y ejecuta la instalación mínima requerida para poder ejecutar las Fases de post-instalación.

Las Fases se encuentran divididas en dos, ya que se requiere que se instale un mínimo de herramientas como lo son node, golang entre otras, que se usarán en la fase dos para instalar más paquetes respectivos.

Esta versión del proyecto respalda mis archivos de configuración para linux pensado primeramente y optimizado para la distro de linux Fedora, pero la idea es que sea multi-sistema, para incluir las distros más famosas de linux, mac y windows



## Estructura de Archviso del proyecto

El proyecto cuenta con una estructura personalizada adaptada para proyectos python

```bash
dotfiles
.
├── common
│   ├── flatpak_installer.py
│   ├── __init__.py
│   ├── install_dotfiles.py
│   ├── installer_config.json
│   ├── install_packages.py
│   ├── logger_utils.py
│   ├── logo.py
│   ├── system_info.py
│   └── system_operations.py
├── config                        # Mi configuración personalizada del sistema operativo
│   ├── alacritty
│   │   ├── alacritty.old
│   │   ├── alacritty.toml
│   │   ├── alacritty.yml
│   │   ├── colorschemes
│   │   ├── colors.yml
│   │   ├── fonts.toml
│   │   ├── fonts.yml
│   │   └── rice-colors.toml
│   ├── bspwm
│   │   ├── assets
│   │   ├── bspwmrc
│   │   ├── dunstrc
│   │   ├── eww
│   │   ├── jgmenurc
│   │   ├── picom.conf
│   │   ├── .rice
│   │   ├── rices
│   │   ├── scripts
│   │   └── sxhkdrc
│   ├── fastfetch
│   │   ├── backup.sh
│   │   ├── config.jsonc
│   │   ├── difference.sh
│   │   ├── logo.png
│   │   ├── progress.sh
│   │   ├── sentu-logo.png
│   │   ├── theme.sh
│   │   ├── timer.sh
│   │   ├── ubuntu.png
│   │   ├── ubuntu.webp
│   │   └── update.sh
│   ├── gh
│   │   ├── config.yml
│   │   └── hosts.yml
│   ├── git
│   │   ├── gitconfig
│   │   └── gitignore_global
│   ├── kitty
│   │   ├── current-theme.conf
│   │   └── kitty.conf
│   ├── lazygit
│   │   └── config.yml
│   ├── mpd
│   │   ├── log
│   │   ├── mpd.conf
│   │   ├── mpd.db
│   │   ├── mpdstate
│   │   └── playlists
│   ├── ncmpcpp
│   │   └── config
│   ├── nvim
│   │   ├── init.lua
│   │   ├── lazy-lock.json
│   │   ├── lazyvim.json
│   │   ├── LICENSE
│   │   ├── lua
│   │   ├── .neoconf.json
│   │   └── stylua.toml
│   ├── ohmyposh
│   │   ├── craver.omp.json
│   │   ├── emodipt-extend.omp.json
│   │   ├── json.omp.json
│   │   ├── negligible.omp.json
│   │   ├── zen.toml
│   │   └── zen.toml.bak
│   ├── paru
│   │   └── paru.conf
│   ├── ranger
│   │   ├── colorschemes
│   │   ├── plugins
│   │   ├── rc.conf
│   │   ├── rifle.conf
│   │   └── scope.sh
│   ├── sentu
│   │   └── logo.sh
│   ├── tmux
│   │   ├── plugins
│   │   └── tmux.conf
│   ├── tmuxinator
│   │   ├── angular.yml
│   │   ├── django.yml
│   │   ├── eureka.yml
│   │   ├── sentu.yml
│   │   └── upwork.yml
│   └── zsh
│       ├── zcompdump
│       └── zhistory
├── docs
│   ├── ISSUE_TEMPLATE
│   │   ├── 🐞-bug-report.md
│   │   ├── 💡-solicitud-de-función.md
│   │   └── 🎯-solicitud-de-pull-request.md
│   └── workflows
│       └── ci.yml
├── home                        # Archivos de configuración personalizada para mi sistema operativo
│   ├── .p10k.zsh
│   └── .zshrc
├── LICENSE
├── logs
├── phase1
│   ├── __init__.py
│   └── main.py
├── phase2
│   ├── __init__.py
│   └── main.py
├── pyproject.toml
├── .python-version
├── README.md
├── .ruff_cache
├── ruff.toml
├── scripts
│   ├── run_phase2.ps1
│   └── run_phase2.sh
└── sentu_install.py

```

# 

# Instalación

```bash
curl -s https://raw.githubusercontent.com/elepistemedev/dotfiles/refs/heads/feature/better_man/sentu_install.py | python3
```
