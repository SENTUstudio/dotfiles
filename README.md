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
├── ansible
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
├── .git
│   ├── COMMIT_EDITMSG
│   ├── config
│   ├── description
│   ├── HEAD
│   ├── hooks
│   ├── index
│   ├── info
│   ├── logs
│   ├── objects
│   └── refs
├── home
│   ├── .p10k.zsh
│   └── .zshrc
├── README.md
└── sentu_install.py
```

#

# Instalación

```bash
curl -s https://raw.githubusercontent.com/elepistemedev/dotfiles/refs/heads/feature/better_man/sentu_install.py | python3
```
