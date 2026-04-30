#!/usr/bin/env python3
import argparse
import platform
import subprocess
import sys
import os
from pathlib import Path
from typing import Optional
import logging
import shutil

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define constants
REPO_URL = "https://github.com/SENTUstudio/dotfiles.git"
DOTFILES_DIR = Path.home() / "dotfiles"
REPO_NAME = "dotfiles"
REPO_BRANCH = (
    "main"  # "main", "develop" | Variable para la rama, se puede modificar aquí
)


def show(message: str = "con Python 🐍"):
    """
    Muestra el logo del proyecto junto a un mensaje personalizado.

    Args:
        message (str): El mensaje que se mostrará debajo del logo.
    """
    encabezado = "Ingeniería de Datos & Data Science"
    mensaje = message

    # Determinar la longitud máxima
    max_len = max(len(encabezado), len(mensaje))

    # Centrar ambas cadenas según la longitud máxima
    encabezado_ajustado = encabezado.center(max_len)
    mensaje_ajustado = mensaje.center(max_len)

    logging.info(
        f"    \033[1m\033[33m█▀ █▀▀ █▄░█ ▀█▀ █░█\033[0m  ┎┤ {encabezado_ajustado} ├┒"
    )
    logging.info(
        f"    \033[1m\033[33m▄█ ██▄ █░▀█ ░█░ █▄█\033[0m  ┖┤ \033[1m{mensaje_ajustado}\033[0m├┚"
    )
    logging.info("                .studio")


def check_command(command: str) -> bool:
    """Verifica si un comando está disponible en el sistema.

    Args:
        command (str): El nombre del comando a verificar.

    Returns:
        bool: True si el comando está disponible, False en caso contrario.
    """
    try:
        subprocess.run(["which", command], capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def run_command(command_list: list[str], cwd: Optional[Path] = None) -> None:
    """Ejecuta un comando en el sistema.

    Args:
        command_list (list[str]): Lista de strings que representan el comando y sus argumentos.
        cwd (Optional[Path]): Directorio de trabajo para ejecutar el comando.

    Raises:
        SystemExit: Si el comando falla.
    """
    try:
        subprocess.run(command_list, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        logging.error(
            f"Error al ejecutar el comando '{' '.join(command_list)}' en '{cwd if cwd else '.'}': {e}"
        )
        sys.exit(1)


def install_yay_python():
    """Instala yay en Arch Linux utilizando Python.

    Esta función automatiza el proceso de instalación de yay, un popular
    ayudante para el AUR (Arch User Repository), realizando los siguientes pasos:
    1. Asegura que los paquetes 'git' y 'base-devel' estén instalados.
    2. Clona el repositorio de yay desde el AUR en un directorio temporal.
    3. Navega al directorio clonado.
    4. Construye e instala yay utilizando 'makepkg -si'.
    5. (Opcional) Limpia el directorio temporal después de la instalación.

    Requiere privilegios de superusuario (sudo) para instalar paquetes
    y ejecutar makepkg. También asume que 'git' está instalado en el sistema.
    """
    try:
        logging.info("Asegurando que git y base-devel estén instalados...")
        subprocess.run(
            ["sudo", "pacman", "-S", "--needed", "git", "base-devel", "--noconfirm"],
            check=True,
        )
        logging.info("git y base-devel instalados o ya presentes.")

        yay_dir = Path.home() / ".cache" / "yay"

        if not yay_dir.exists():
            logging.info("Clonando el repositorio de yay desde AUR...")
            subprocess.run(
                ["git", "clone", "https://aur.archlinux.org/yay.git", str(yay_dir)],
                check=True,
            )
            logging.info("Repositorio de yay clonado.")
        else:
            logging.info("El repositorio de yay ya existe.")

        logging.info("Navegando al directorio de yay...")
        os.chdir(str(yay_dir))

        logging.info("Construyendo e instalando yay...")
        subprocess.run(["makepkg", "-si", "--noconfirm"], check=True)
        logging.info("Yay instalado exitosamente.")

        # Opcional: Limpiar el directorio clonado
        logging.info("Limpiando el directorio de construcción de yay...")
        os.chdir(str(Path.home()))
        shutil.rmtree(yay_dir)
        logging.info("Limpieza completada.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error durante la instalación: {e}")
    except FileNotFoundError as e:
        logging.error(f"Comando no encontrado: {e}")
    except Exception as e:
        logging.error(f"Ocurrió un error inesperado: {e}")


def install_uv():
    """Instala uv (gestor de paquetes Python ultra-rápido de Astral) via script curl."""
    install_uv_cmd = 'curl -LsSf https://astral.sh/uv/install.sh | sh'
    command_list = ["bash", "-c", install_uv_cmd]
    logging.info("Instalando uv...")
    run_command(command_list)


def package_core():
    """Verifica e instala Git si no está presente.

    Cross-platform bootstrap:
    - Linux: detecta el gestor de paquetes nativo (apt, dnf, pacman, etc.)
             e instala git, luego uv.
    - Darwin (macOS): verifica Homebrew; si falta, ejecuta el instalador
      oficial de Homebrew. Luego instala git via brew y uv via curl.
      Nunca se requieren privilegios de administrador explícitos porque
      el installer de Homebrew solicita elevación si es necesario.
    - Windows: no soportado; instrucciones manuales.
    """
    os_name = platform.system()

    logging.info("Instalando dependencias...")
    if os_name == "Linux":
        package_managers = {
            "apt-get": ["sudo", "apt-get", "update"],
            "dnf": ["sudo", "dnf", "update", "-y"],
            "pacman": ["sudo", "pacman", "-Syy", "--noconfirm"],
            "yum": ["sudo", "yum", "update", "-y"],
            "zypper": ["sudo", "zypper", "update", "-y"],
        }
        install_commands = {
            "apt-get": ["sudo", "apt-get", "install", "-y", "git"],
            "dnf": ["sudo", "dnf", "install", "-y", "git", "python3-libdnf5"],
            "pacman": ["sudo", "pacman", "-S", "--noconfirm", "git"],
            "yum": ["sudo", "yum", "install", "-y", "git"],
            "zypper": ["sudo", "zypper", "install", "-y", "git"],
        }
        install_uv()
        for pm, update_cmd in package_managers.items():
            if check_command(pm):
                logging.info(
                    f"Gestor de paquetes '{pm}' detectado. Intentando instalar Paquetes..."
                )
                run_command(update_cmd)
                run_command(install_commands[pm])

                if pm == "pacman":
                    show("💾 Instalando yay")
                    install_yay_python()

                if check_command("git"):
                    logging.info("Git instalado exitosamente.")
                    return True
                logging.error(f"Falló la instalación de Git con '{pm}'.")
                break  # Salir del bucle si se intentó con un gestor de paquetes
        else:
            logging.error(
                "No se reconoció un gestor de paquetes compatible para la instalación automática de Git."
            )
            logging.info(
                "Por favor, instala Git manualmente y vuelve a ejecutar el script."
            )
            sys.exit(1)
    elif os_name == "Darwin":
        # -----------------------------------------------------------------
        # DARWIN BOOTSTRAP FLOW (macOS)
        # -----------------------------------------------------------------
        # 1. Homebrew es el gestor de paquetes estándar en macOS.
        #    Si no está instalado, ejecutamos el script oficial de
        #    https://brew.sh que maneja automáticamente la arquitectura
        #    (Intel vs Apple Silicon) y las rutas (/usr/local vs /opt/homebrew).
        # 2. Una vez Homebrew disponible, instalamos git via brew para
        #    asegurar una versión actual y compatible.
        # 3. uv se instala universalmente (Linux y Darwin) via su script
        #    curl oficial, manteniendo paridad entre plataformas.
        # -----------------------------------------------------------------

        # Bootstrap Homebrew en macOS si no está presente
        brew_installed_now = False
        if not check_command("brew"):
            logging.info("Homebrew no encontrado. Ejecutando instalador oficial...")
            try:
                subprocess.run(
                    [
                        "/bin/bash",
                        "-c",
                        '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)',
                    ],
                    check=True,
                )
                logging.info("Homebrew instalado exitosamente.")
                brew_installed_now = True
            except subprocess.CalledProcessError as e:
                logging.error(f"Error instalando Homebrew: {e}")
                sys.exit(1)
        else:
            logging.info("Homebrew ya está instalado.")

        # Asegurar que brew está en PATH (especialmente en Apple Silicon después de instalación fresca)
        if brew_installed_now:
            machine = platform.machine()
            if machine == "arm64":
                brew_bin = "/opt/homebrew/bin"
            else:
                brew_bin = "/usr/local/bin"
            if brew_bin not in os.environ.get("PATH", ""):
                os.environ["PATH"] = f"{brew_bin}:{os.environ.get('PATH', '')}"
                logging.info(f"Agregado {brew_bin} al PATH para esta sesión.")

        # Instalar git y python3 via Homebrew (siempre, no solo si brew ya existía)
        logging.info("Instalando git y python3 via Homebrew...")
        try:
            subprocess.run(["brew", "install", "git", "python3"], check=True)
            logging.info("Git y Python 3 instalados exitosamente via Homebrew.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error instalando git/python3 via Homebrew: {e}")
            sys.exit(1)

        # Instalar uv en macOS
        install_uv()
        return True
    elif os_name == "Windows":
        logging.info(
            "Por favor, instala Git en Windows (por ejemplo, desde https://git-scm.com/download/win)."
        )
        logging.info("Luego, vuelve a ejecutar este script.")
        sys.exit(1)
    else:
        logging.error(
            f"Sistema operativo '{os_name}' no reconocido para la instalación automática de Git."
        )
        logging.info(
            "Por favor, instala Git manualmente y vuelve a ejecutar el script."
        )
        sys.exit(1)
    return False  # Debería haber salido antes si la instalación falla


def clone_repo():
    """Clona el repositorio de dotfiles, manejando el caso de que ya exista."""
    if DOTFILES_DIR.exists():
        if (DOTFILES_DIR / ".git").exists():
            try:
                # Verificar si el origen remoto es el correcto
                remote_url = subprocess.run(
                    ["git", "config", "--get", "remote.origin.url"],
                    cwd=str(DOTFILES_DIR),
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip()
                if remote_url == REPO_URL:
                    logging.info(
                        f"El repositorio ya existe en '{DOTFILES_DIR}' y apunta al origen correcto. Intentando actualizar..."
                    )
                    run_command(
                        ["git", "config", "pull.rebase", "true"], cwd=DOTFILES_DIR
                    )
                    run_command(["git", "pull"], cwd=DOTFILES_DIR)
                    logging.info("Repositorio actualizado exitosamente.")
                    return
                else:
                    logging.warning(
                        f"El repositorio existe en '{DOTFILES_DIR}' pero apunta a '{remote_url}'. Se restablecerá el origen."
                    )
                    run_command(
                        ["git", "remote", "set-url", "origin", REPO_URL],
                        cwd=DOTFILES_DIR,
                    )
                    logging.info("Origen remoto restablecido. Intentando actualizar...")
                    run_command(
                        ["git", "config", "pull.rebase", "true"], cwd=DOTFILES_DIR
                    )
                    run_command(["git", "pull"], cwd=DOTFILES_DIR)
                    logging.info("Repositorio actualizado exitosamente.")
                    return
            except subprocess.CalledProcessError as e:
                logging.error(f"Error al interactuar con el repositorio existente: {e}")
                logging.info("Se intentará clonar el repositorio nuevamente.")
                # No hacemos sys.exit aquí, intentamos clonar de nuevo

        logging.warning(
            f"El directorio '{DOTFILES_DIR}' existe pero no parece ser un repositorio Git completo. Intentando eliminar y clonar de nuevo."
        )
        try:
            shutil.rmtree(DOTFILES_DIR, ignore_errors=False)
        except OSError as e:
            logging.error(f"Error al eliminar el directorio existente: {e}")
            logging.error(
                "Por favor, verifica los permisos o elimina el directorio manualmente."
            )
            sys.exit(1)

    logging.info(
        f"Clonando el repositorio '{REPO_NAME}' desde '{REPO_URL}' a '{DOTFILES_DIR}' en la rama '{REPO_BRANCH}'..."
    )
    try:
        run_command(["git", "clone", "-b", REPO_BRANCH, REPO_URL, str(DOTFILES_DIR)])
        logging.info("Repositorio clonado exitosamente.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al clonar el repositorio: {e}")
        sys.exit(1)


def install_go():
    """Instala Go si no está presente (simplificado para dotfiles-only)."""
    if check_command("go"):
        return True

    logging.info("Go no encontrado. Instalando Go...")
    os_name = platform.system()
    machine = platform.machine()

    arch_map = {"x86_64": "amd64", "arm64": "arm64", "aarch64": "arm64"}
    go_arch = arch_map.get(machine, machine)

    os_map = {"Linux": "linux", "Darwin": "darwin"}
    go_os = os_map.get(os_name, os_name.lower())

    go_version = "1.23.4"
    tarball = f"go{go_version}.{go_os}-{go_arch}.tar.gz"
    url = f"https://go.dev/dl/{tarball}"

    try:
        logging.info(f"Descargando Go {go_version}...")
        run_command(["curl", "-fsSL", url, "-o", f"/tmp/{tarball}"])
        logging.info("Extrayendo Go...")
        run_command(["sudo", "rm", "-rf", "/usr/local/go"])
        run_command(["sudo", "tar", "-C", "/usr/local", "-xzf", f"/tmp/{tarball}"])
        run_command(["rm", "-f", f"/tmp/{tarball}"])

        # Agregar al PATH para esta sesión
        os.environ["PATH"] = "/usr/local/go/bin:" + os.environ.get("PATH", "")

        if check_command("go"):
            logging.info("Go instalado correctamente.")
            return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error instalando Go: {e}")

    logging.error("No se pudo instalar Go automáticamente.")
    logging.info("Instalalo manualmente desde https://go.dev/dl/ y volvé a intentar.")
    return False


def ensure_sentu_dotfiles():
    """Asegura que sentu-dotfiles esté compilado e instalado en ~/.local/bin/."""
    install_dir = Path.home() / ".local" / "bin"
    binary = install_dir / "sentu-dotfiles"

    if binary.exists():
        logging.info(f"sentu-dotfiles encontrado en {binary}")
        return str(binary)

    logging.info("sentu-dotfiles no encontrado. Compilando desde el repositorio...")

    if not install_go():
        sys.exit(1)

    install_dir.mkdir(parents=True, exist_ok=True)

    try:
        run_command(
            ["go", "build", "-ldflags=-s -w", "-o", str(binary), "./cmd/sentu-dotfiles"],
            cwd=DOTFILES_DIR,
        )
        binary.chmod(0o755)
        logging.info(f"sentu-dotfiles compilado e instalado en {binary}")
        return str(binary)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error compilando sentu-dotfiles: {e}")
        sys.exit(1)


def install_dotfiles_only():
    """Instala solo los dotfiles usando sentu-dotfiles (sin Ansible)."""
    logging.info("Modo dotfiles-only: desplegando con sentu-dotfiles...")

    binary = ensure_sentu_dotfiles()

    # Asegurar que ~/.local/bin está en PATH para esta sesión
    local_bin = str(Path.home() / ".local" / "bin")
    if local_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{local_bin}:{os.environ.get('PATH', '')}"

    logging.info("Ejecutando sentu-dotfiles deploy...")
    try:
        run_command([binary, "deploy"])
        logging.info("Dotfiles desplegados exitosamente.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error desplegando dotfiles: {e}")
        sys.exit(1)


def run_ansible_playbook(test: bool = False, check: bool = False):
    """Ejecuta el playbook de Ansible si Ansible está instalado."""
    ansible_dir = DOTFILES_DIR / "ansible"
    if test:
        playbook_path = ansible_dir / "playbook-test.yml"
    else:
        playbook_path = ansible_dir / "playbook.yml"
    inventory_file_path = (
        ansible_dir / "inventory.ini"
    )  # Asumo que el inventario está en la misma carpeta
    uv_path = os.path.expanduser("~/.local/bin")
    os.environ["PATH"] = f"{os.environ['PATH']}:{uv_path}"
    uv_sync = ["uv", "sync"]
    run_command(uv_sync, cwd=DOTFILES_DIR)

    # if not check_command("ansible-playbook"):
    #     logging.error("Ansible no está instalado, no se puede ejecutar el playbook.")
    #     return False

    if not playbook_path.exists():
        logging.error(f"No se encontró el playbook de Ansible en: {playbook_path}")
        return False

    if not inventory_file_path.exists():
        logging.warning(
            f"No se encontró el archivo de inventario en: {inventory_file_path}. Ansible podría fallar."
        )

    logging.info("Ejecutando Ansible Playbook...")
    try:
        command = [
            "uv",
            "run",
            "ansible-playbook",
            "--ask-become-pass",
        ]
        if check:
            command.append("--check")
        command.append(str(playbook_path))
        # "-vvv",
        # "-v",
        run_command(command, cwd=DOTFILES_DIR)
        logging.info("Ansible Playbook ejecutado exitosamente.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar Ansible Playbook: {e}")
        return False


def install_questionary() -> bool:
    """Instala Questionary y PyYAML via uv para soportar el TUI interactivo.

    Returns:
        bool: True si la instalación fue exitosa, False en caso contrario.
    """
    logging.info("Instalando dependencias de TUI (questionary, pyyaml)...")
    try:
        subprocess.run(
            ["uv", "pip", "install", "questionary", "pyyaml"],
            check=True,
            capture_output=True,
            text=True,
        )
        logging.info("Dependencias de TUI instaladas correctamente.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.warning(f"No se pudieron instalar las dependencias de TUI: {e}")
        return False


def redirect_tty() -> bool:
    """Redirige stdin a /dev/tty si no es un TTY interactivo.

    Esto permite que Questionary funcione correctamente cuando el script
    se ejecuta via pipe (ej: curl | python3).

    Returns:
        bool: True si se garantizó un TTY usable, False si falló.
    """
    if not sys.stdin.isatty():
        try:
            sys.stdin = open("/dev/tty", "r")
            logging.info("stdin redirigido a /dev/tty para modo interactivo.")
            return True
        except OSError as e:
            logging.warning(f"No se pudo redirigir a /dev/tty: {e}")
            return False
    return True


def run_tui_picker(os_family: str) -> Optional[dict]:
    """Ejecuta el picker TUI de dos niveles para seleccionar aplicaciones.

    Lee el archivo de variables de la distro detectada, presenta un checkbox
    de categorías y luego un checkbox por categoría seleccionada para elegir
    apps individuales. Finalmente genera selection.yaml.

    Args:
        os_family (str): Familia del SO detectada (RedHat, Archlinux, Debian, Darwin).

    Returns:
        Optional[dict]: Diccionario con las selecciones del usuario, o None si
                     el usuario canceló o no hay TTY disponible.
    """
    # Fallback si no hay TTY usable
    if not redirect_tty():
        logging.warning("No se detectó TTY. Se instalará todo completo.")
        return None

    if not install_questionary():
        logging.warning("Fallback a instalación completa por falla de dependencias TUI.")
        return None

    try:
        import questionary
        import yaml
    except ImportError as e:
        logging.warning(f"No se pudo importar {e.name}. Fallback a instalación completa.")
        return None

    vars_path = DOTFILES_DIR / "ansible" / "vars" / f"{os_family}.yaml"
    if not vars_path.exists():
        logging.error(f"No se encontró el archivo de variables: {vars_path}")
        return None

    with open(vars_path, "r", encoding="utf-8") as f:
        distro_vars = yaml.safe_load(f)

    dependencies = distro_vars.get("package_managers", {}).get("dependencies", {})
    categorized = dependencies.get("categorized", {})
    categorized_cask = dependencies.get("categorized_cask", {})

    # Fallback a extended si no hay categorized (backward compat)
    if not categorized:
        logging.warning("No se encontró 'categorized' en vars. Fallback a instalación completa.")
        return None

    # Construir lista de categorías no vacías (merge brew + cask en Darwin)
    categories = {}
    for cat, apps in categorized.items():
        if apps:
            categories.setdefault(cat, {"brew": [], "cask": []})
            categories[cat]["brew"] = apps
    for cat, apps in categorized_cask.items():
        if apps:
            categories.setdefault(cat, {"brew": [], "cask": []})
            categories[cat]["cask"] = apps

    if not categories:
        logging.warning("No hay categorías disponibles. Fallback a instalación completa.")
        return None

    # --- Primer nivel: selección de categorías ---
    cat_choices = sorted(categories.keys())
    selected_cats = questionary.checkbox(
        "Seleccioná las categorías que querés instalar:",
        choices=cat_choices,
    ).ask()

    if selected_cats is None:
        logging.info("El usuario canceló la selección de categorías.")
        return None

    if not selected_cats:
        logging.info("No se seleccionó ninguna categoría.")
        return {"selected_packages": [], "selected_cask_packages": [], "selected_categories": []}

    # --- Segundo nivel: selección de apps por categoría ---
    selected_packages = []
    selected_cask_packages = []
    selected_categories = []
    by_category = {}

    for cat in selected_cats:
        cat_data = categories[cat]
        all_apps = []
        if cat_data["brew"]:
            all_apps.extend([(app, "brew") for app in cat_data["brew"]])
        if cat_data["cask"]:
            all_apps.extend([(app, "cask") for app in cat_data["cask"]])

        if not all_apps:
            continue

        app_choices = [
            questionary.Choice(title=app, value=(app, pkg_type))
            for app, pkg_type in all_apps
        ]

        selected_apps = questionary.checkbox(
            f"Seleccioná las apps de {cat}:",
            choices=app_choices,
        ).ask()

        if selected_apps is None:
            logging.info(f"El usuario canceló la selección para {cat}.")
            continue

        if selected_apps:
            selected_categories.append(cat)
            by_category[cat] = {"brew": [], "cask": []}
            for app, pkg_type in selected_apps:
                if pkg_type == "cask":
                    selected_cask_packages.append(app)
                    by_category[cat]["cask"].append(app)
                else:
                    selected_packages.append(app)
                    by_category[cat]["brew"].append(app)

    result = {
        "selected_packages": selected_packages,
        "selected_cask_packages": selected_cask_packages,
        "selected_categories": selected_categories,
        "by_category": by_category,
    }
    return result


def show_summary(selections: dict) -> bool:
    """Muestra un resumen agrupado por categoría y pide confirmación.

    Args:
        selections (dict): Diccionario con selected_packages, selected_cask_packages
                           y selected_categories.

    Returns:
        bool: True si el usuario confirmó, False si quiere salir o no hay selecciones.
    """
    if not selections:
        return False

    selected_packages = selections.get("selected_packages", [])
    selected_cask_packages = selections.get("selected_cask_packages", [])
    selected_categories = selections.get("selected_categories", [])

    total = len(selected_packages) + len(selected_cask_packages)

    if total == 0:
        print("\n⚠️  No seleccionaste ninguna app.")
        while True:
            resp = input("¿Querés volver al menú o salir? [v/s]: ").strip().lower()
            if resp in ("v", "volver"):
                return False  # Indica que se debe volver al menú
            if resp in ("s", "salir"):
                logging.info("Saliendo sin realizar cambios.")
                sys.exit(0)
            print("Opción inválida. Ingresá 'v' para volver o 's' para salir.")

    print("\n" + "=" * 50)
    print("  Resumen de instalación")
    print("=" * 50)

    by_category = selections.get("by_category", {})
    for cat in selected_categories:
        print(f"\n📁 {cat}")
        cat_data = by_category.get(cat, {})
        for app in cat_data.get("brew", []):
            print(f"   • {app}")
        for app in cat_data.get("cask", []):
            print(f"   • {app} (cask)")

    print(f"\nTotal: {total} aplicaciones seleccionadas.")

    while True:
        resp = input("\n¿Confirmás la instalación? [Y/n]: ").strip().lower()
        if resp in ("", "y", "yes", "s", "si"):
            return True
        if resp in ("n", "no"):
            while True:
                resp2 = input("¿Querés volver al menú o salir? [v/s]: ").strip().lower()
                if resp2 in ("v", "volver"):
                    return False
                if resp2 in ("s", "salir"):
                    logging.info("Saliendo sin realizar cambios.")
                    sys.exit(0)
                print("Opción inválida. Ingresá 'v' para volver o 's' para salir.")
        print("Opción inválida. Ingresá 'Y' para confirmar o 'n' para cancelar.")


def write_selection_yaml(selections: dict) -> Optional[Path]:
    """Escribe el archivo ansible/vars/selection.yaml con las selecciones.

    Args:
        selections (dict): Diccionario con las listas de paquetes seleccionados.

    Returns:
        Optional[Path]: Ruta del archivo escrito, o None si no había selecciones.
    """
    if not selections:
        return None

    ansible_vars_dir = DOTFILES_DIR / "ansible" / "vars"
    ansible_vars_dir.mkdir(parents=True, exist_ok=True)
    selection_path = ansible_vars_dir / "selection.yaml"

    content = {
        "selected_packages": selections.get("selected_packages", []),
        "selected_cask_packages": selections.get("selected_cask_packages", []),
        "selected_categories": selections.get("selected_categories", []),
    }

    try:
        import yaml
        with open(selection_path, "w", encoding="utf-8") as f:
            yaml.dump(content, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        logging.info(f"Archivo de selección guardado en: {selection_path}")
        return selection_path
    except ImportError:
        logging.error("PyYAML no está disponible. No se pudo escribir selection.yaml.")
        return None


def show_menu() -> str:
    """Muestra el menú interactivo y devuelve la opción seleccionada."""
    print("\n" + "=" * 50)
    print("  SENTU Dotfiles Installer")
    print("=" * 50)
    print("\nSelecciona una opción:")
    print("  [1] Instalación completa (sistema + dotfiles)")
    print("  [2] Solo dotfiles (copiar configs, saltar paquetes)")
    print("  [3] Modo test (ansible --check)")
    print("  [4] Salir")
    print("  [5] Instalación personalizada (elegir apps)")
    print()

    while True:
        try:
            choice = input("Opción [1-5]: ").strip()
            if choice in {"1", "2", "3", "4", "5"}:
                return choice
            print("Opción inválida. Por favor ingresa un número del 1 al 5.")
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            sys.exit(0)


def setup_only_mode(os_family: str | None) -> None:
    """Ejecuta la instalación completa sin menú interactivo.

    Este modo es invocado por sentu-dotfiles setup (Go) para que
    Python se encargue del setup y Go del deploy de dotfiles.
    """
    if not package_core():
        logging.error("No se pudo instalar dependencias. Saliendo.")
        sys.exit(1)

    show("💾 Clonación de dotfiles iniciada")
    clone_repo()
    logging.info("💾 Clonación de dotfiles terminada")

    # Si hay TTY y detectamos OS family, mostramos picker
    if os_family is not None and sys.stdin.isatty():
        show("🎨 Iniciando selección personalizada de aplicaciones")
        selections = run_tui_picker(os_family)
        if selections is not None:
            if show_summary(selections):
                write_selection_yaml(selections)
                show("⚙️  Iniciando instalación personalizada")
                run_ansible_playbook(test=False)
                show("✅ Instalación de paquetes completada")
                return
            # Si el usuario no confirmó, fallback a full
            logging.info("El usuario canceló la selección personalizada. Fallback a full.")

    show("⚙️  Iniciando instalación de paquetes")
    run_ansible_playbook(test=False)
    show("✅ Instalación de paquetes completada")


def main():
    parser = argparse.ArgumentParser(
        description="SENTU Dotfiles Installer - Instalación completa del sistema"
    )
    parser.add_argument(
        "--setup-only",
        action="store_true",
        help="Ejecuta solo la instalación de paquetes (sin menú). Usado por sentu-dotfiles.",
    )
    args = parser.parse_args()

    # Redirigir stdin desde /dev/tty si estamos en un pipe (ej: curl | python3)
    # para que input() y questionary funcionen correctamente.
    redirect_tty()

    show()
    os_name = platform.system()
    logging.info(f"Sistema operativo detectado: {os_name}")

    # Detectar OS family
    os_family = None
    if os_name == "Darwin":
        os_family = "Darwin"
    elif os_name == "Linux":
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("ID="):
                        distro_id = line.strip().split("=", 1)[1].strip('"')
                        if distro_id in ("fedora", "rhel", "centos", "rocky", "almalinux"):
                            os_family = "RedHat"
                        elif distro_id == "arch":
                            os_family = "Archlinux"
                        elif distro_id in ("debian", "ubuntu", "pop", "mint"):
                            os_family = "Debian"
                        break
        except FileNotFoundError:
            pass

    if args.setup_only:
        setup_only_mode(os_family)
        return

    while True:
        choice = show_menu()

        if choice == "4":
            logging.info("Saliendo sin realizar cambios.")
            sys.exit(0)

        if choice == "2":
            # Dotfiles-only: solo necesitamos git y clonar
            if not check_command("git"):
                logging.error("Git no está instalado. Instálalo manualmente y vuelve a intentar.")
                sys.exit(1)
            show("💾 Clonación de dotfiles iniciada")
            clone_repo()
            logging.info("💾 Clonación de dotfiles terminada")
            install_dotfiles_only()
            show("✅ Dotfiles instalados. Disfruta tu configuración!")
            return

        if choice == "3":
            # Test mode
            if not package_core():
                logging.error("No se pudo instalar dependencias. Saliendo.")
                sys.exit(1)
            show("💾 Clonación de dotfiles iniciada")
            clone_repo()
            logging.info("💾 Clonación de dotfiles terminada")
            show("⚙️  Iniciando instalación de paquetes (modo test --check)")
            run_ansible_playbook(test=False, check=True)
            show("✅ Modo test completado. Revisa la salida de Ansible.")
            return

        if choice == "5":
            # Instalación personalizada con picker TUI
            if not package_core():
                logging.error("No se pudo instalar dependencias. Saliendo.")
                sys.exit(1)
            show("💾 Clonación de dotfiles iniciada")
            clone_repo()
            logging.info("💾 Clonación de dotfiles terminada")

            if os_family is None:
                logging.error("No se pudo detectar la familia del sistema operativo para el picker.")
                logging.info("Fallback a instalación completa.")
                show("⚙️  Iniciando instalación de paquetes")
                run_ansible_playbook(test=False)
                show("✅ Configuración completa. Te invito a reiniciar tu sistema y disfrutar")
                return

            selections = run_tui_picker(os_family)
            if selections is None:
                logging.info("Fallback a instalación completa.")
                show("⚙️  Iniciando instalación de paquetes")
                run_ansible_playbook(test=False)
                show("✅ Configuración completa. Te invito a reiniciar tu sistema y disfrutar")
                return

            if not show_summary(selections):
                # El usuario eligió volver al menú
                continue

            write_selection_yaml(selections)
            show("⚙️  Iniciando instalación personalizada")
            run_ansible_playbook(test=False)
            show("✅ Configuración completa. Te invito a reiniciar tu sistema y disfrutar")
            return

        # choice == "1" (default full install)
        if not package_core():
            logging.error("No se pudo instalar dependencias. Saliendo.")
            sys.exit(1)

        show("💾 Clonación de dotfiles iniciada")
        clone_repo()
        logging.info("💾 Clonación de dotfiles terminada")

        show("⚙️  Iniciando instalación de paquetes")
        run_ansible_playbook(test=False)
        show("✅ Configuración completa. Te invito a reiniciar tu sistema y disfrutar")


if __name__ == "__main__":
    main()
