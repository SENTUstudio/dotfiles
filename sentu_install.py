#!/usr/bin/env python3
import platform
import subprocess
import sys
from pathlib import Path

# Define constants
REPO_URL = "https://github.com/SENTUstudio/dotfiles.git"
DOTFILES_DIR = Path.home() / "dotfiles"
REPO_NAME = "dotfiles"


def show(message: str = "con Python 🐍"):
    encabezado = "Ingeniería de Datos & Data Science"
    mensaje = message
    max_len = max(len(encabezado), len(mensaje))
    encabezado_ajustado = encabezado.center(max_len)
    mensaje_ajustado = mensaje.center(max_len)
    logo = f"""
    \033[1m\033[33m█▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤ DATA ENGINEER
    ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤ Obteniendo datos para empresas, personas... para ti ├┚
                    STUDIO
    \033[0m
    {encabezado_ajustado}
    {mensaje_ajustado}
    """
    print(logo)


def check_command(command: str) -> bool:
    try:
        subprocess.run([command, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def run_command(command_list: list):
    try:
        subprocess.run(command_list, check=True)
    except subprocess.CalledProcessError as e:
        error(f"Error al ejecutar el comando '{' '.join(command_list)}': {e}")
        sys.exit(1)


def info(message: str):
    print(f"\033[1;34m[INFO]\033[0m {message}")


def error(message: str):
    print(f"\033[1;31m[ERROR]\033[0m {message}")


def clone_repo():
    if DOTFILES_DIR.exists():
        info(
            f"El directorio '{DOTFILES_DIR}' ya existe. ¿Deseas eliminarlo y clonar de nuevo? (s/N)"
        )
        response = input().lower()
        if response == "s":
            try:
                info(f"Eliminando '{DOTFILES_DIR}'...")
                subprocess.run(["rm", "-rf", str(DOTFILES_DIR)], check=True)
            except subprocess.CalledProcessError as e:
                error(f"Error al eliminar el directorio: {e}")
                sys.exit(1)
        else:
            info("Omitiendo la clonación del repositorio.")
            return

    info(
        f"Clonando el repositorio '{REPO_NAME}' desde '{REPO_URL}' a '{DOTFILES_DIR}'..."
    )
    try:
        subprocess.run(["git", "clone", REPO_URL, str(DOTFILES_DIR)], check=True)
        info("Repositorio clonado exitosamente.")
    except subprocess.CalledProcessError as e:
        error(f"Error al clonar el repositorio: {e}")
        sys.exit(1)


def check_and_install_ansible():
    if not check_command("ansible-playbook"):
        info("Ansible no está instalado. Intentando instalarlo con pip...")
        os_name = platform.system()
        match os_name:
            case "Linux":
                try:
                    subprocess.run(
                        ["python3", "-m", "pip", "install", "ansible"], check=True
                    )
                    info("Ansible instalado exitosamente (pip).")

                    info(
                        "Verificando gestor de paquetes para dependencias de Ansible..."
                    )
                    match (
                        check_command("apt-get"),
                        check_command("dnf"),
                        check_command("pacman"),
                        check_command("yum"),
                    ):
                        case (False, True, False, False):
                            info(
                                "Gestor de paquetes 'dnf' detectado. Intentando instalar python3-libdnf5..."
                            )
                            run_command(
                                ["sudo", "dnf", "install", "-y", "python3-libdnf5"]
                            )
                            info("python3-libdnf5 instalado exitosamente.")
                        case _:
                            info(
                                "No se detectó un gestor de paquetes conocido que requiera dependencias específicas para Ansible."
                            )
                    return True
                except subprocess.CalledProcessError as e:
                    error(f"Error al instalar Ansible con pip: {e}")
                    info(
                        "Asegúrate de tener pip instalado y configurado correctamente."
                    )
                    info(
                        "Si los problemas persisten, intenta instalar Ansible manualmente usando el gestor de paquetes de tu distribución."
                    )
                    return False
            case "Darwin":
                info(
                    "Por favor, instala Ansible en macOS usando pip: `pip3 install ansible`."
                )
                info("Luego, vuelve a ejecutar este script.")
                return False
            case "Windows":
                info(
                    "Por favor, instala Ansible en Windows usando pip: `pip install ansible`."
                )
                info("Luego, vuelve a ejecutar este script.")
                return False
            case _:
                error(
                    f"Sistema operativo '{os_name}' no reconocido para la instalación automática de Ansible."
                )
                info(
                    "Por favor, instala Ansible manualmente (preferiblemente con pip) y vuelve a ejecutar este script."
                )
                return False
    else:
        info("Ansible ya está instalado.")
        return True


def main():
    show()
    os_name = platform.system()
    info(f"Sistema operativo detectado: {os_name}")

    info("Verificando si Git está instalado...")
    match os_name:
        case "Linux":
            if not check_command("git"):
                info(
                    "Git no está instalado. Intentando instalarlo con el gestor de paquetes..."
                )
                match (
                    check_command("apt-get"),
                    check_command("dnf"),
                    check_command("pacman"),
                    check_command("yum"),
                ):
                    case (True, False, False, False):
                        info(
                            "Gestor de paquetes 'apt' detectado. Intentando instalar Git..."
                        )
                        run_command(["sudo", "apt-get", "update"])
                        run_command(["sudo", "apt-get", "install", "-y", "git"])
                    case (False, True, False, False):
                        info(
                            "Gestor de paquetes 'dnf' detectado. Intentando instalar Git..."
                        )
                        run_command(["sudo", "dnf", "update", "-y"])
                        run_command(["sudo", "dnf", "install", "-y", "git"])
                    case (False, False, True, False):
                        info(
                            "Gestor de paquetes 'pacman' detectado. Intentando instalar Git..."
                        )
                        run_command(["sudo", "pacman", "-Syy", "--noconfirm"])
                        run_command(["sudo", "pacman", "-S", "--noconfirm", "git"])
                    case (False, False, False, True):
                        info(
                            "Gestor de paquetes 'yum' detectado. Intentando instalar Git..."
                        )
                        run_command(["sudo", "yum", "update", "-y"])
                        run_command(["sudo", "yum", "install", "-y", "git"])
                    case _:
                        error(
                            "Gestor de paquetes no reconocido para la instalación automática de Git."
                        )
                        info(
                            "Por favor, instala Git manualmente y vuelve a ejecutar el script."
                        )
                        sys.exit(1)
            else:
                info("Git ya está instalado.")
        case "Darwin":
            if not check_command("git"):
                info(
                    "Por favor, instala Git en macOS (por ejemplo, usando Xcode Command Line Tools o Homebrew)."
                )
                info("Luego, vuelve a ejecutar este script.")
                sys.exit(1)
            else:
                info("Git ya está instalado.")
        case "Windows":
            if not check_command("git"):
                info(
                    "Por favor, instala Git en Windows (por ejemplo, desde https://git-scm.com/download/win)."
                )
                info("Luego, vuelve a ejecutar este script.")
                sys.exit(1)
            else:
                info("Git ya está instalado.")
        case _:
            error(
                f"Sistema operativo '{os_name}' no reconocido para la instalación automática de Git."
            )
            info("Por favor, instala Git manualmente y vuelve a ejecutar este script.")
            sys.exit(1)

    clone_repo()
    show("💾 Clonación de dotfiles terminada")

    inventory_file = create_inventory()

    if check_and_install_ansible() and inventory_file:
        ansible_dir = DOTFILES_DIR / "ansible" / "playbook.yml"

        if playbook_path.exists():
            info("Ejecutando Ansible Playbook...")
            try:
                subprocess.run(
                    [
                        "ansible-playbook",
                        "--ask-become-pass",
                        str(playbook_path),
                        "-i",
                        inventory_file,
                    ],
                    cwd=str(ansible_dir),
                    check=True,
                )
                info("Ansible Playbook ejecutado exitosamente.")
            except subprocess.CalledProcessError as e:
                error(f"Error al ejecutar Ansible Playbook: {e}")
                sys.exit(1)
        else:
            error(f"No se encontró el playbook de Ansible en: {playbook_path}")
            sys.exit(1)
    else:
        error(
            "No se puede continuar sin Ansible instalado o sin el archivo de inventario."
        )
        sys.exit(1)

    show("✅ Configuración completa")


def create_inventory():
    inventory_path = DOTFILES_DIR / "ansible" / "inventory.ini"
    info(f"Creando archivo de inventario en: {inventory_path}")
    try:
        with open(inventory_path, "w") as f:
            f.write("[local]\nlocalhost ansible_connection=local\n")
        info("Archivo de inventario creado exitosamente.")
        return str(inventory_path)
    except Exception as e:
        error(f"Error al crear el archivo de inventario: {e}")
        return None


if __name__ == "__main__":
    main()
