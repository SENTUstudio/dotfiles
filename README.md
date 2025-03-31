```
  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤  Ingeniería de Datos & Data Science  ├┒
  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤              en Python               ├┚
              .studio
```

<div align="center"><p>
    <a href="https://github.com/SENTUstudio/dotfiles/releases/latest">
      <img alt="Última versión" src="docs/badges/version.svg" />
    </a>
    <a href="https://github.com/SENTUstudio/dotfiles/pulse">
      <img alt="Último commit" src="docs/badges/last-commit.svg"/>
    </a>
    <a href="https://github.com/SENTUstudio/dotfiles/blob/main/LICENSE">
      <img alt="Licencia" src="docs/badges/license.svg" />
    </a>
    <a href="https://github.com/SENTUstudio/dotfiles/stargazers">
      <img alt="Estrellas" src="docs/badges/stars.svg" />
    </a>
    <a href="https://github.com/SENTUstudio/dotfiles/issues">
      <img alt="Problemas" src="docs/badges/issues.svg" />
    </a>
    <a href="https://github.com/SENTUstudio/dotfiles">
      <img alt="Tamaño del repositorio" src="docs/badges/repo-size.svg" />
    </a>
  </p>
</div>

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
    %% Define styles for C4-like appearance
    classDef person fill:#08427B,color:#fff,stroke:#052E56,stroke-width:2px
    classDef externalSystem fill:#999999,stroke:#666666,stroke-width:2px
    classDef container fill:#438DD5,color:#fff,stroke:#2E6295,stroke-width:2px
    classDef component fill:#85BBF0,color:#000,stroke:#5A8CBF,stroke-width:2px
    classDef database fill:#FF8F40,color:#000,stroke:#CC7A3C,stroke-width:2px
    classDef boundary fill:none,stroke:#444,stroke-width:2px,stroke-dasharray:5 5

    %% Installation Process with C4 styling
    subgraph boundary_install ["Proceso de Instalación"]
        A["sentu_install.py\n[Script Instalador]"]:::component
        A -->|"ejecuta"| B["Motor de Ansible Playbook\n[Motor de Orquestación]"]:::container
    end

    %% Configuration File with C4 styling
    subgraph boundary_config ["Configuración"]
        B10["installer_config.yaml\n[Base de Datos de Configuración]"]:::database
    end

    %% Ansible Components with C4 styling
    subgraph boundary_ansible ["Componentes del Motor de Ansible"]
        B1["playbook.yml\n[Playbook Principal]"]:::component
        B2["test\n[Role de Pruebas]"]:::component
        B3["base_system_configuration\n[Role de Configuración Base]"]:::component
        B4["add_repositories\n[Role de Configuración de Repositorios]"]:::component
        B5["install_core_dependencies\n[Role de Dependencias Core]"]:::component
        B6["install_uv\n[Role de Python UV]"]:::component
        B7["install_rye\n[Role de Python Rye]"]:::component
        B8["install_extended_dependencies\n[Role de Dependencias Extendidas]"]:::component
        B9["install_post_install\n[Role de Post-Instalación]"]:::component
        B11["install_fonts\n[Role de Instalación de Fuentes]"]:::component
        B12["dotfiles_management\n[Role de Gestión de Dotfiles]"]:::component
    end

    %% Deployment Targets with C4 styling
    subgraph boundary_deploy ["Destinos de Implementación"]
        C["Archivos de Configuración\n[Configuración del Sistema]"]:::container
        D["Dotfiles del Usuario\n[Entorno de Usuario]"]:::container
    end

    %% Update the flow based on the new playbook order
    B --> B1
    B1 --> B10
    B10 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5
    B5 --> B6
    B6 --> B7
    B7 --> B8
    B8 --> B9
    B9 --> B11
    B11 --> B12

    B12 -->|"despliega"| C
    B12 -->|"copia a"| D

    %% Set boundary style
    style boundary_install fill:none,stroke:#777,stroke-width:2px,stroke-dasharray:7 5
    style boundary_config fill:none,stroke:#777,stroke-width:2px,stroke-dasharray:7 5
    style boundary_ansible fill:none,stroke:#777,stroke-width:2px,stroke-dasharray:7 5
    style boundary_deploy fill:none,stroke:#777,stroke-width:2px,stroke-dasharray:7 5

    %% Hyperlinks
    click A "https://github.com/sentustudio/dotfiles/blob/main/sentu_install.py"
    click B1 "https://github.com/sentustudio/dotfiles/blob/main/ansible/playbook.yml"
    click B2 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/test"
    click B3 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/base_system_configuration"
    click B4 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/add_repositories"
    click B5 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_core_dependencies"
    click B6 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_uv"
    click B7 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_rye"
    click B8 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_extended_dependencies"
    click B9 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_post_install"
    click B10 "https://github.com/sentustudio/dotfiles/blob/main/ansible/vars/installer_config.yaml"
    click B11 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/install_fonts"
    click B12 "https://github.com/sentustudio/dotfiles/tree/main/ansible/roles/dotfiles_management"
    click C "https://github.com/sentustudio/dotfiles/tree/main/config"
    click D "https://github.com/sentustudio/dotfiles/tree/main/home"
```
