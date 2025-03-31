```
█▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤ DATA ENGINEER                                       ├┒
▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤ Obteniendo datos para empresas, personas... para ti ├┚
                STUDIO
```

# dotfiles

Proyecto que se encarga de hacer una post-instalación a un sistema operativo resién instalado, donde instala las aplicaciones bases de mi preferencia y copia mis archivos de configuración al nuevo sistema. consta de un script llamado sentu_install.py que se usa por medio de curl para llamar a todo el proyecto en formato zip desde un repositorio, lo extrae y ejecuta la instalación mínima requerida para poder ejecutar las Fases de post-instalación.

Su funcionamiento es simple, con la instrucción de instalar (mencionada más abajo) se toma el script sentu_install.py desde el repositorio y se ejecuta, donde comprueba los requerimientos mínimos para su funcionamiento y si no los tiene los instala, luego clona el repositorio dotfiles y ejecuta Ansible para realizar la post-instalación de paquetes y enlaces de mis archivos config

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

Sistemas Operativos probados

- [x] Fedora KDE 41+

- [ ] OpenSUSE

# Instalación

```bash
curl -LsSf https://raw.githubusercontent.com/SENTUstudio/dotfiles/refs/heads/main/sentu_install.py | python3
```

# Diagrama de flujo

```mermaid
flowchart TD
    subgraph "Installation Process"
        A["sentu_install.py"]:::installer
        A -->|"calls"| B["Ansible Playbook Engine"]:::ansible
    end

    subgraph "Ansible Engine Components"
        B1["Playbook: playbook.yml"]:::playbook
        B2["Role: add_repositories"]:::role
        B3["Role: base_system_configuration"]:::role
        B4["Role: install_core_dependencies"]:::role
        B5["Role: install_extended_dependencies"]:::role
        B6["Role: dotfiles_management"]:::role
        B7["Role: install_post_install"]:::role
        B8["Role: install_rye"]:::role
        B9["Role: install_uv"]:::role
        B10["Vars: installer_config.yaml"]:::vars
    end

    B --> B1
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5
    B5 --> B6
    B6 --> B7
    B7 --> B8
    B8 --> B9
    B2 --- B10

    subgraph "Deployment Targets"
        C["Configuration Files (config)"]:::config
        D["User Home Dotfiles (home)"]:::home
    end

    B6 -->|"deploys"| C
    B6 -->|"copies_to"| D

    click A "https://github.com/sentustudio/dotfiles/blob/main/sentu_install.py"
    click B1 "https://github.com/sentustudio/dotfiles/blob/main/ansible/playbook.yml"
    click B2 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/add_repositories"
    click B3 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/base_system_configuration"
    click B4 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_core_dependencies"
    click B5 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_extended_dependencies"
    click B6 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/dotfiles_management"
    click B7 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_post_install"
    click B8 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_rye"
    click B9 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_uv"
    click B10 "https://github.com/sentustudio/dotfiles/blob/main/ansible/vars/installer_config.yaml"
    click C "https://github.com/sentustudio/dotfiles/tree/main/config"
    click D "https://github.com/sentustudio/dotfiles/tree/main/home"

    classDef installer fill:#ffcc00,stroke:#333,stroke-width:2px;
    classDef ansible fill:#99ccff,stroke:#333,stroke-width:2px;
    classDef playbook fill:#ddffdd,stroke:#333,stroke-width:2px;
    classDef role fill:#cce5ff,stroke:#333,stroke-width:2px;
    classDef vars fill:#ffcccc,stroke:#333,stroke-width:2px;
    classDef config fill:#e6ccff,stroke:#333,stroke-width:2px;
    classDef home fill:#ffe6cc,stroke:#333,stroke-width:2px;
```
