#!/usr/bin/env python3
import os
import platform
import subprocess
import sys

REPO_URL = "URL_DEL_REPOSITORIO_GIT"  # Reemplaza con la URL real de tu repositorio
DOTFILES_DIR = os.path.expanduser("~/dotfiles")
REPO_NAME = REPO_URL.split("/")[-1].replace(".git", "")


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


def info(message):
    print(f"\033[1;34m[INFO]\033[0m {message}")


def error(message):
    print(f"\033[1;31m[ERROR]\033[0m {message}")


def check_command(command):
    """Verifica si un comando está disponible en el sistema.

    Args:
        command (str): El nombre del comando a verificar.

    Returns:
        bool: True si el comando está disponible, False en caso contrario.
    """
    try:
        subprocess.run(["which", command], capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def run_command(command_list, check=True):
    """Ejecuta un comando y verifica si hubo errores.

    Args:
        command_list (list[str]): Una lista que representa el comando y sus argumentos.
        check (bool, optional): Indica si se debe verificar el código de salida. Defaults to True.

    Returns:
        subprocess.CompletedProcess: El objeto CompletedProcess resultante de la ejecución del comando.
    """
    result = subprocess.run(command_list, capture_output=True, text=True)
    if check and result.returncode != 0:
        error(f"Error al ejecutar: {' '.join(command_list)}")
        error(f"Stdout: {result.stdout}")
        error(f"Stderr: {result.stderr}")
        sys.exit(1)
    info(f"Ejecutado: {' '.join(command_list)}")
    if result.stdout:
        info(f"Stdout: {result.stdout}")
    return result


def main():
    show("💾 Instalación de dotfiles")
    if not check_command("curl"):
        error("curl no está instalado. Por favor, instálalo para continuar.")
        sys.exit(1)

    if os.path.exists(DOTFILES_DIR):
        info(f"La carpeta de dotfiles ya existe en {DOTFILES_DIR}.")
        info(
            "Si deseas reinstalar, por favor, elimina la carpeta y vuelve a ejecutar el script."
        )
        sys.exit(0)

    os_name = platform.system()

    match os_name:
        case "Linux":
            if not check_command("git"):
                info("Git no está instalado. Intentando instalar...")
                info("Detectando gestor de paquetes...")

                match (
                    check_command("apt-get"),
                    check_command("dnf"),
                    check_command("pacman"),
                    check_command("yum"),
                ):
                    case (True, _, _, _):
                        info(
                            "Gestor de paquetes 'apt' detectado. Intentando instalar Git..."
                        )
                        run_command(["sudo", "apt-get", "update"])
                        run_command(["sudo", "apt-get", "install", "-y", "git"])
                    case (_, True, _, _):
                        info(
                            "Gestor de paquetes 'dnf' detectado. Intentando instalar Git..."
                        )
                        run_command(["sudo", "dnf", "update", "-y"])
                        run_command(["sudo", "dnf", "install", "-y", "git"])
                    case (_, _, True, _):
                        info(
                            "Gestor de paquetes 'pacman' detectado. Intentando instalar Git..."
                        )
                        run_command(["sudo", "pacman", "-Syy", "--noconfirm"])
                        run_command(["sudo", "pacman", "-S", "--noconfirm", "git"])
                    case (_, _, _, True):
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


if __name__ == "__main__":
    main()
