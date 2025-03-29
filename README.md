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
├── ansible
│   ├── playbook.yml
│   ├── roles
│   │   ├── add_repositories
│   │   │   └── tasks
│   │   │       └── main.yml
│   │   ├── base_system_configuration
│   │   │   └── tasks
│   │   │       └── main.yml
│   │   ├── dotfiles_management
│   │   │   └── tasks
│   │   │       └── main.yml
│   │   ├── install_core_dependencies
│   │   │   └── tasks
│   │   │       └── main.yml
│   │   ├── install_extended_dependencies
│   │   │   └── tasks
│   │   │       └── main.yml
│   │   ├── install_post_install
│   │   │   └── tasks
│   │   │       └── main.yml
│   │   ├── install_rye
│   │   │   └── tasks
│   │   │       └── main.yml
│   │   └── install_uv
│   │       └── tasks
│   │           └── main.yml
│   └── vars
│       └── installer_config.yaml
├── config
│   ├── alacritty
│   ├── bspwm
│   ├── fastfetch
│   ├── gh
│   ├── git
│   ├── kitty
│   ├── lazygit
│   ├── mpd
│   ├── ncmpcpp
│   ├── nvim
│   ├── ohmyposh
│   ├── paru
│   ├── ranger
│   ├── sentu
│   ├── tmux
│   ├── tmuxinator
│   └── zsh
├── home
│   ├── .p10k.zsh
│   └── .zshrc
├── README.md
└── sentu_install.py

```

#

# Instalación

```bash
curl -LsSf https://raw.githubusercontent.com/SENTUstudio/dotfiles/refs/heads/main/sentu_install.py | python3
```
