# Tart Testing Infrastructure

> Testing framework para validar dotfiles en macOS (via Tart) y Fedora (via Docker fallback).
> Branch: `feature/mac-install`

---

## Requisitos

### macOS (host de pruebas)

- **Apple Silicon** (M1/M2/M3/M4) — Tart solo funciona en arm64.
- **macOS 13+** — Recomendado para compatibilidad con Sequoia images.
- **Homebrew** — Para instalar Tart.
- **Tart CLI**:
  ```bash
  brew install cirruslabs/cli/tart
  ```

### Opcional: Docker (fallback Fedora)

- Docker Desktop o Docker Engine para el fallback de regresión Linux.

---

## Estructura

```
tests/tart/
├── setup-macos-base.sh         # Task 4.2 — Clona imagen base de Cirrus Labs
├── snapshot-macos-clean.sh     # Task 4.3 — Crea golden snapshot post-setup
├── run-macos-test.sh           # Task 4.4 — Ejecuta sentu_install.py en VM limpia
├── run-fedora-regression.sh    # Task 4.5 — Valida que Linux no se rompió
├── cleanup.sh                  # Task 4.6 — Elimina VMs de prueba
└── README.md                   # Task 4.7 — Este documento
```

---

## Flujo de Trabajo

### 1. Crear VM base (una sola vez)

Descarga la imagen oficial `macos-sequoia-base` desde el registry de Cirrus Labs:

```bash
cd tests/tart
./setup-macos-base.sh
```

Esto crea la VM local **`dotfiles-macos-base`**.

### 2. Crear golden snapshot (una sola vez)

Arranca la VM base una vez para que macOS complete su configuración inicial, luego clona el resultado como imagen inmutable:

```bash
./snapshot-macos-clean.sh
```

Esto crea **`dotfiles-macos-clean`** — el punto de partida para todos los tests.

> **IMPORTANTE:** No modifiques `dotfiles-macos-clean` manualmente. Si necesitas regenerarla, vuelve a ejecutar este script.

### 3. Ejecutar test de macOS

Cada ejecución clona desde el golden snapshot, corre el instalador, y destruye la VM temporal:

```bash
./run-macos-test.sh
```

**Qué hace internamente:**
1. Clona `dotfiles-macos-clean` → `dotfiles-macos-test-<timestamp>`
2. Arranca la VM y espera su IP
3. Copia el proyecto `dotfiles/` vía `rsync`
4. Ejecuta `python3 sentu_install.py` (actualmente envía opción `4` = Salir para evitar bloqueo; cámbialo a `1` o `3` para pruebas reales)
5. Apaga y elimina la VM temporal
6. Imprime **PASS** o **FAIL**

### 4. Ejecutar regresión Fedora

Valida que los paths de Linux no se rompieron con los cambios de macOS:

```bash
./run-fedora-regression.sh
```

**Estrategia:**
1. Intenta usar una VM Fedora registrada en Tart (si existe).
2. Si no hay VM Fedora, usa **Docker** como fallback:
   - Levanta contenedor `fedora:latest`
   - Instala `ansible`, `git`, `python3`
   - Ejecuta `ansible-playbook --syntax-check playbook-test.yml`
   - Ejecuta `ansible-playbook playbook-test.yml` (sin `--check` por limitaciones de contenedor)
   - Destruye el contenedor

### 5. Limpiar VMs de prueba

Elimina todas las VMs temporales preservando la base y el golden snapshot:

```bash
./cleanup.sh
```

**Preservadas siempre:**
- `dotfiles-macos-base`
- `dotfiles-macos-clean`

**Eliminadas:**
- `dotfiles-macos-test-*`
- `dotfiles-fedora-test-*`

---

## Automatización Completa (CI local)

Para correr todo el ciclo de validación de una sola vez:

```bash
cd tests/tart
./setup-macos-base.sh      # solo la primera vez
./snapshot-macos-clean.sh  # solo la primera vez
./run-macos-test.sh
./run-fedora-regression.sh
./cleanup.sh
```

---

## Troubleshooting

| Síntoma | Causa probable | Solución |
|---------|---------------|----------|
| `tart: command not found` | Tart no instalado | `brew install cirruslabs/cli/tart` |
| Timeout en boot | Primera ejecución muy lenta | Aumentar `BOOT_TIMEOUT` en el script |
| SSH rechaza conexión | VM aún no terminó setup | Esperar 10-15s extra después de obtener IP |
| `rsync` no encontrado | Falta rsync en host | `brew install rsync` |
| Docker fallback falla | Docker no corre | Iniciar Docker Desktop o agregar usuario al grupo docker |
| Ansible syntax-check falla | Error YAML en playbook | Revisar `ansible-playbook --syntax-check` localmente |

---

## Referencias

- [Tart Documentation](https://tart.run/)
- [Cirrus Labs macOS Images](https://github.com/cirruslabs/macos-image-templates)
- [Dotfiles Ansible Playbook](../../ansible/playbook.yml)
- [Sentu Installer](../../sentu_install.py)
