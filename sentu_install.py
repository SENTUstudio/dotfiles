#!/usr/bin/env python3
import platform
import subprocess
import sys
from pathlib import Path
import logging

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define constants
REPO_URL = "https://github.com/SENTUstudio/dotfiles.git"
DOTFILES_DIR = Path.home() / "dotfiles"
REPO_NAME = "dotfiles"
REPO_BRANCH = "main"  # Variable para la rama, se puede modificar aquí


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

    logo = f"""
    \033[1m\033[33m█▀ █▀▀ █▄░█ ▀█▀ █░█\033[0m  ┎┤ {encabezado_ajustado} ├┒
    \033[1m\033[33m▄█ ██▄ █░▀█ ░█░ █▄█\033[0m  ┖┤ \033[1m{mensaje_ajustado}\033[0m├┚
                .studio
    """
    print(logo)


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


def install_git():
    """Verifica e instala Git si no está presente."""
    os_name = platform.system()
    logging.info("Verificando si Git está instalado...")
    if check_command("git"):
        logging.info("Git ya está instalado.")
        return True

    logging.info("Git no está instalado. Intentando instalarlo...")
    match os_name:
        case "Linux":
            package_managers = {
                "apt-get": ["sudo", "apt-get", "update"],
                "dnf": ["sudo", "dnf", "update", "-y"],
                "pacman": ["sudo", "pacman", "-Syy", "--noconfirm"],
                "yum": ["sudo", "yum", "update", "-y"],
                "zypper": ["sudo", "zypper", "update", "-y"],
            }
            install_commands = {
                "apt-get": ["sudo", "apt-get", "install", "-y", "git"],
                "dnf": ["sudo", "dnf", "install", "-y", "git"],
                "pacman": ["sudo", "pacman", "-S", "--noconfirm", "git"],
                "yum": ["sudo", "yum", "install", "-y", "git"],
                "zypper": ["sudo", "zypper", "install", "-y", "git"],
            }
            for pm, update_cmd in package_managers.items():
                if check_command(pm):
                    logging.info(
                        f"Gestor de paquetes '{pm}' detectado. Intentando instalar Git..."
                    )
                    run_command(update_cmd)
                    run_command(install_commands[pm])
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
        case "Darwin":
            logging.info(
                "Por favor, instala Git en macOS (por ejemplo, usando Xcode Command Line Tools o Homebrew)."
            )
            logging.info("Luego, vuelve a ejecutar este script.")
            sys.exit(1)
        case "Windows":
            logging.info(
                "Por favor, instala Git en Windows (por ejemplo, desde https://git-scm.com/download/win)."
            )
            logging.info("Luego, vuelve a ejecutar este script.")
            sys.exit(1)
        case _:
            logging.error(
                f"Sistema operativo '{os_name}' no reconocido para la instalación automática de Git."
            )
            logging.info(
                "Por favor, instala Git manualmente y vuelve a ejecutar este script."
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


def install_ansible():
    """Verifica e intenta instalar Ansible si no está presente."""
    if check_command("ansible-playbook"):
        logging.info("Ansible ya está instalado.")
        return True

    logging.info("Ansible no está instalado. Intentando instalarlo con pip...")
    os_name = platform.system()
    try:
        run_command(
            ["python3", "-m", "pip", "install", "ansible", "--break-system-packages"]
        )
        if check_command("ansible-playbook"):
            logging.info("Ansible instalado exitosamente (pip).")
            return True
        else:
            logging.error("La instalación de Ansible con pip parece haber fallado.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al instalar Ansible con pip: {e}")
        logging.info("Asegúrate de tener pip instalado y configurado correctamente.")

    logging.info(
        "Si los problemas persisten, intenta instalar Ansible manualmente usando el gestor de paquetes de tu distribución:"
    )
    if os_name == "Linux":
        logging.info(
            "- Para Debian/Ubuntu: `sudo apt-get update && sudo apt-get install -y ansible`"
        )
        logging.info(
            "- Para Fedora/CentOS/RHEL: `sudo dnf install -y ansible` o `sudo yum install -y ansible`"
        )
        logging.info("- Para Arch Linux: `sudo pacman -S ansible`")
        logging.info("- Para openSUSE: `sudo zypper install ansible`")
    elif os_name == "Darwin":
        logging.info(
            "- Para macOS: `pip3 install ansible` (si tienes pip3 instalado) o considera usar Homebrew: `brew install ansible`"
        )
    elif os_name == "Windows":
        logging.info(
            "- Para Windows: `pip install ansible` (asegúrate de que pip esté configurado correctamente)"
        )
    else:
        logging.info(
            f"- No se proporcionaron instrucciones específicas para '{os_name}'. Consulta la documentación de Ansible para tu sistema operativo."
        )

    logging.error(
        "Por favor, instala Ansible manualmente y vuelve a ejecutar el script."
    )
    return False


def run_ansible_playbook():
    """Ejecuta el playbook de Ansible si Ansible está instalado."""
    ansible_dir = DOTFILES_DIR / "ansible"
    playbook_path = ansible_dir / "playbook.yml"
    inventory_file_path = (
        ansible_dir / "inventory.ini"
    )  # Asumo que el inventario está en la misma carpeta

    if not check_command("ansible-playbook"):
        logging.error("Ansible no está instalado, no se puede ejecutar el playbook.")
        return False

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
            "ansible-playbook",
            "--ask-become-pass",
            str(playbook_path),
            "-i",
            str(inventory_file_path),
            "-v",
        ]
        run_command(command, cwd=ansible_dir)
        logging.info("Ansible Playbook ejecutado exitosamente.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar Ansible Playbook: {e}")
        return False


def main():
    show()
    os_name = platform.system()
    logging.info(f"Sistema operativo detectado: {os_name}")

    if not install_git():
        logging.error("No se pudo instalar Git. Saliendo.")
        sys.exit(1)

    clone_repo()
    show("💾 Clonación de dotfiles terminada")

    if install_ansible():
        if not run_ansible_playbook():
            logging.error("La ejecución del Ansible Playbook falló o no se realizó.")
    else:
        logging.warning(
            "No se pudo instalar Ansible. La configuración automática podría no completarse."
        )

    show("✅ Configuración completa")


if __name__ == "__main__":
    main()
