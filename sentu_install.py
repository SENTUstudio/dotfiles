#!/usr/bin/env python3
import platform
import subprocess
import sys
import os
from pathlib import Path
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
    "develop"  # "main", "develop" | Variable para la rama, se puede modificar aquí
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


def run_command(command_list: list[str], cwd: Path | None = None) -> None:
    """Ejecuta un comando en el sistema.

    Args:
        command_list (list[str]): Lista de strings que representan el comando y sus argumentos.
        cwd (Path | None): Directorio de trabajo para ejecutar el comando.

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
            except subprocess.CalledProcessError as e:
                logging.error(f"Error instalando Homebrew: {e}")
                sys.exit(1)
        else:
            logging.info("Homebrew ya está instalado.")

            # Instalar git y python3 via Homebrew
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
            run_command(["rm", "-rf", str(DOTFILES_DIR)])
        except subprocess.CalledProcessError as e:
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


def install_dotfiles_only():
    """Instala solo los dotfiles creando enlaces simbólicos (sin Ansible)."""
    logging.info("Modo dotfiles-only: creando enlaces simbólicos...")

    config_src = DOTFILES_DIR / "config"
    config_dst = Path.home() / ".config"
    home_src = DOTFILES_DIR / "home"
    home_dst = Path.home()

    # Asegurar que los directorios destino existen
    config_dst.mkdir(parents=True, exist_ok=True)

    # Crear enlaces simbólicos para directorios y archivos en config/
    if config_src.exists():
        for item in config_src.iterdir():
            dest = config_dst / item.name
            if dest.exists() or dest.is_symlink():
                logging.info(f"Eliminando existente: {dest}")
                if dest.is_dir() and not dest.is_symlink():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            logging.info(f"Creando enlace simbólico: {dest} -> {item}")
            os.symlink(item, dest)

    # Crear enlaces simbólicos para archivos en home/
    if home_src.exists():
        for item in home_src.iterdir():
            dest = home_dst / item.name
            if dest.exists() or dest.is_symlink():
                logging.info(f"Eliminando existente: {dest}")
                if dest.is_dir() and not dest.is_symlink():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            logging.info(f"Creando enlace simbólico: {dest} -> {item}")
            os.symlink(item, dest)

    logging.info("Dotfiles instalados exitosamente.")


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
    print()

    while True:
        try:
            choice = input("Opción [1-4]: ").strip()
            if choice in {"1", "2", "3", "4"}:
                return choice
            print("Opción inválida. Por favor ingresa 1, 2, 3 o 4.")
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            sys.exit(0)


def main():
    show()
    os_name = platform.system()
    logging.info(f"Sistema operativo detectado: {os_name}")

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
