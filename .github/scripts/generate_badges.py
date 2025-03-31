"""
Genera badges estáticos para el README de un repositorio privado.

Este script utiliza la API de GitHub para obtener métricas del repositorio
y genera badges estáticos en formato SVG usando la biblioteca `pybadges`.
Los badges se almacenan en la carpeta `docs/badges/` y el README se actualiza
para referenciar los nuevos badges.

Uso:
    python generate_badges.py <GITHUB_TOKEN>
"""

import os
import re

from pybadges import badge
import requests

# Constantes
REPO_NAME = os.getenv("GITHUB_REPOSITORY")
BADGES_DIR = "docs/badges"
README_PATH = "README.md"


def fetch_latest_release(token):
    """Obtiene la última versión del repositorio."""
    url = f"https://api.github.com/repos/{REPO_NAME}/releases/latest"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        # No hay releases disponibles
        return "No releases"

    response.raise_for_status()  # Lanza una excepción para otros errores HTTP
    return response.json()["tag_name"]


def fetch_last_commit(token):
    """Obtiene el hash del último commit del repositorio."""
    url = f"https://api.github.com/repos/{REPO_NAME}/commits"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()[0]["sha"][:7]  # Retorna los primeros 7 caracteres


def fetch_repo_info(token):
    """Obtiene información general del repositorio (licencia, estrellas, tamaño)."""
    url = f"https://api.github.com/repos/{REPO_NAME}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return {
        "license": data["license"]["spdx_id"] if data["license"] else "None",
        "stars": data["stargazers_count"],
        "size": f"{data['size']} KB",
    }


def generate_badge(label, value, filename, color=None):
    """Genera un badge estático en formato SVG con un color específico."""
    # Determinar el color basado en el valor del badge
    if label == "Coverage":
        if value == "unknown":
            color = "CCCCCC"  # Gris para valores desconocidos
        else:
            color = (
                "8bd5ca" if float(value) >= 80 else "FF0000"
            )  # Verde si ≥ 80%, rojo si < 80%
    elif color is None:
        if label == "CI":
            color = (
                "8bd5ca"
                if value == "passing"
                else "FF0000"
                if value == "failing"
                else "CCCCCC"
            )
        elif label == "Issues":
            color = "F5E0DC" if value == "0" else "FF0000"
        elif label == "Versión":
            color = "C9CBFF"
        elif label == "Último Commit":
            color = "8bd5ca"
        elif label == "Licencia":
            color = "ee999f"
        elif label == "Estrellas":
            color = "c69ff5"
        elif label == "Tamaño":
            color = "DDB6F2"
        else:
            color = "CCCCCC"  # Color predeterminado

    # Generar el badge
    badge_svg = badge(left_text=label, right_text=str(value), right_color=f"#{color}")
    os.makedirs(BADGES_DIR, exist_ok=True)
    filepath = os.path.join(BADGES_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(badge_svg)
    return filepath


def update_readme():
    """Actualiza el README para usar los badges estáticos generados."""
    with open(README_PATH, encoding="utf-8") as f:
        readme_content = f.read()

    # Reemplazar solo el atributo `src` de cada badge
    readme_content = re.sub(
        r'src="https://img\.shields\.io/github/v/release/[^"]+"',
        'src="docs/badges/version.svg"',
        readme_content,
    )
    readme_content = re.sub(
        r'src="https://img\.shields\.io/github/last-commit/[^"]+"',
        'src="docs/badges/last-commit.svg"',
        readme_content,
    )
    readme_content = re.sub(
        r'src="https://img\.shields\.io/github/license/[^"]+"',
        'src="docs/badges/license.svg"',
        readme_content,
    )
    readme_content = re.sub(
        r'src="https://img\.shields\.io/github/stars/[^"]+"',
        'src="docs/badges/stars.svg"',
        readme_content,
    )
    readme_content = re.sub(
        r'src="https://img\.shields\.io/github/issues/[^"]+"',
        'src="docs/badges/issues.svg"',
        readme_content,
    )
    readme_content = re.sub(
        r'src="https://img\.shields\.io/github/repo-size/[^"]+"',
        'src="docs/badges/repo-size.svg"',
        readme_content,
    )
    readme_content = re.sub(
        r'src="https://img\.shields\.io/github/actions/workflow/status/[^"]+"',
        'src="docs/badges/ci-status.svg"',
        readme_content,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)


def main():
    """Función principal del script."""
    token = os.getenv("GITHUB_TOKEN")
    print(f"Token obtenido: {token}")  # Depuración: Imprime el token obtenido
    if not token:
        raise ValueError("El token GITHUB_TOKEN no está configurado.")

    try:
        # Obtener datos del repositorio
        latest_release = fetch_latest_release(token)
        last_commit = fetch_last_commit(token)
        repo_info = fetch_repo_info(token)

        # Generar badges con colores dinámicos
        generate_badge("Versión", latest_release, "version.svg")
        generate_badge("Último Commit", last_commit, "last-commit.svg")
        generate_badge("Licencia", repo_info["license"], "license.svg")
        generate_badge("Estrellas", str(repo_info["stars"]), "stars.svg")
        generate_badge("Issues", "0", "issues.svg")  # TODO: Implementar conteo real
        generate_badge("Tamaño", repo_info["size"], "repo-size.svg")

        print("Badges generados y README actualizado correctamente.")
    except Exception as e:
        print(f"Error al generar badges: {e}")
        raise


if __name__ == "__main__":
    main()
