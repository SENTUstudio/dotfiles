# Análisis: .zshrc Actual vs Proyecto dotfiles

> Fecha: 2025-04-27
> Rama: feature/mac-install
> Autor: SDD Orchestrator

---

## Resumen Ejecutivo

El `.zshrc` del proyecto es **significativamente diferente** al `.zshrc` actual del usuario. El proyecto usa un stack moderno basado en **zinit + Powerlevel10k**, mientras que el usuario actualmente usa **Oh My Zsh + robbyrussell**. Además, el `.zshrc` del proyecto tiene hardcodeos de paths Linux que rompen en macOS.

| Aspecto | .zshrc Actual (Usuario) | .zshrc Proyecto (dotfiles) | Estado |
|---------|------------------------|---------------------------|--------|
| Framework | Oh My Zsh | zinit + Powerlevel10k | Diferente |
| Plugin manager | Oh My Zsh built-in | zinit | Diferente |
| Tema | robbyrussell | Powerlevel10k | Diferente |
| macOS paths | ✅ Bien | ❌ Hardcodeados Linux | **Necesita fix** |
| Herramientas actuales | Kiro, LM Studio, Antigravity, Neo4j, opencode | No incluidas | **Necesita agregar** |
| Secrets expuestos | Sí (TBK_TOKEN, Neo4j) | No | **Problema de seguridad** |

---

## Hallazgos Críticos

### 🔴 1. Hardcodeo de Paths Linux en macOS

El `.zshrc` del proyecto tiene paths que NO existen en macOS:

```zsh
# Línea 176-177 — SOLO aplica a Linux
export PATH=/usr/lib64/qt6/bin:$PATH
export QT_SELECT=6

# Línea 181 — Hardcodeado a usuario "el"
export PATH="$PATH:/home/el/.lmstudio/bin"

# Línea 184 — Hardcodeado a usuario "el"
export PATH="$PATH:/home/el/go/bin"

# Línea 189 — Linuxbrew comentado pero presente
# eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

# Línea 197 — Hardcodeado a usuario "el"
[ -s "/home/el/.bun/_bun" ] && source "/home/el/.bun/_bun"
```

**Impacto:** En macOS, estos paths no existen y podrían causar errores silenciosos o mensajes de archivo no encontrado.

**Fix necesario:**
```zsh
# Conditional para Linux-only
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    export PATH=/usr/lib64/qt6/bin:$PATH
    export QT_SELECT=6
fi

# Usar $HOME en vez de /home/el
export PATH="$PATH:$HOME/.lmstudio/bin"
export PATH="$PATH:$HOME/go/bin"
```

---

### 🔴 2. Herramientas del Usuario No Incluidas

El usuario actual tiene configuradas herramientas que el proyecto no gestiona:

| Herramienta | En .zshrc actual | En proyecto | Acción |
|-------------|-----------------|-------------|--------|
| **Kiro CLI** | ✅ Líneas 2, 118, 129 | ❌ No existe | Agregar soporte condicional |
| **LM Studio CLI** | ✅ Líneas 114, 181 | ⚠️ Hardcodeado Linux | Usar $HOME condicional |
| **Antigravity** | ✅ Líneas 126, 133 | ❌ No existe | Agregar |
| **Neo4j MCP** | ✅ Líneas 121-123 | ❌ No existe | Agregar (sin credenciales) |
| **OpenCode PATH** | ✅ Línea 136 | ❌ No existe | Agregar |
| **Go** | ✅ Líneas 139-140 | ✅ Línea 184 | Fix path hardcodeado |
| **Cargo** | ✅ Línea 130 | ✅ Línea 173 | OK |
| **NVM** | ✅ Líneas 108-110 | ✅ Líneas 133-139 | Diferente implementación |
| **Bun** | ❌ No existe | ✅ Líneas 197-201 | Proyecto lo agrega |
| **Atuin** | ❌ No existe | ✅ Líneas 168-170 | Proyecto lo agrega |
| **UV** | ❌ No existe | ✅ Líneas 203-205 | Proyecto lo agrega |
| **Rye** | ❌ No existe | ✅ Línea 194 | Proyecto lo agrega |

---

### 🟡 3. Secrets Expuestos en .zshrc Actual

El `.zshrc` actual del usuario tiene **credenciales hardcodeadas**:

```zsh
# Línea 111 — TOKEN expuesto
export TBK_TOKEN="eler6153:BBDC-MzY4NTExNjI0ODUxOkATuN0IhiapeNZAaNSbaNPMPVsq"

# Líneas 121-123 — Credenciales Neo4j
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="sentu_password"
```

**⚠️ Advertencia:** NUNCA versionar secrets. El proyecto debe proveer templates o variables de entorno para esto.

---

### 🟡 4. Diferencia de Arquitectura: Oh My Zsh vs zinit

| Característica | Oh My Zsh (actual) | zinit (proyecto) |
|----------------|-------------------|------------------|
| Velocidad | Lenta (~200-500ms) | Rápida (~50-100ms) |
| Plugins | plugins=() array | zinit light / snippet |
| Temas | ZSH_THEME= | Powerlevel10k |
| Complejidad | Baja | Media-Alta |
| Curva de aprendizaje | Baja | Media |

**Recomendación:** El proyecto ya usa zinit. Mantener zinit pero hacerlo más robusto para macOS.

---

## Recomendaciones de Mejora

### Para el `.zshrc` del proyecto:

1. **Agregar bloque condicional por OS:**
```zsh
# Detectar OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS-specific paths
    export PATH="$PATH:$HOME/.lmstudio/bin"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux-specific paths
    export PATH=/usr/lib64/qt6/bin:$PATH
    export QT_SELECT=6
    export PATH="$PATH:$HOME/.lmstudio/bin"
fi
```

2. **Agregar herramientas faltantes del usuario:**
```zsh
# OpenCode (si está instalado)
if [ -d "$HOME/.opencode/bin" ]; then
    export PATH="$HOME/.opencode/bin:$PATH"
fi

# Antigravity (si está instalado)
if [ -d "$HOME/.antigravity/antigravity/bin" ]; then
    export PATH="$HOME/.antigravity/antigravity/bin:$PATH"
fi

# Kiro CLI (solo macOS)
if [[ "$OSTYPE" == "darwin"* ]] && [[ -f "$HOME/Library/Application Support/kiro-cli/shell/zshrc.pre.zsh" ]]; then
    source "$HOME/Library/Application Support/kiro-cli/shell/zshrc.pre.zsh"
fi
```

3. **No versionar secrets:** Crear `.zshrc.secrets.template` con:
```zsh
# Copiar a ~/.zshrc.secrets y completar
# export TBK_TOKEN=""
# export NEO4J_URI=""
# export NEO4J_USERNAME=""
# export NEO4J_PASSWORD=""
```

4. **Fix paths hardcodeados:** Reemplazar `/home/el/` por `$HOME/` en todo el archivo.

---

## Matriz de Tareas Derivadas

| # | Tarea | Prioridad | Archivo |
|---|-------|-----------|---------|
| 1 | Fix paths Linux hardcodeados en `.zshrc` | Alta | `home/.zshrc` |
| 2 | Agregar bloque condicional `OSTYPE` para macOS/Linux | Alta | `home/.zshrc` |
| 3 | Agregar opencode PATH condicional | Media | `home/.zshrc` |
| 4 | Agregar Kiro CLI condicional (solo macOS) | Media | `home/.zshrc` |
| 5 | Agregar LM Studio PATH con `$HOME` | Media | `home/.zshrc` |
| 6 | Crear `.zshrc.secrets.template` | Media | `home/.zshrc.secrets.template` |
| 7 | Documentar que el usuario debe crear `~/.zshrc.secrets` | Baja | `docs/aplicaciones.md` |

---

## Archivos Referenciados

- `home/.zshrc` — Configuración del proyecto (a mejorar)
- `/Users/elepistemedev/.zshrc` — Configuración actual del usuario
- `config/opencode/` — Configuración de opencode (copiada al proyecto)

---

*Análisis generado durante el desarrollo de feature/mac-install.*
