# SEO Strategy — SENTU Dotfiles

> Fecha: 2025-04-27
> Objetivo: Maximizar descubrimiento orgánico en GitHub Search, Google, y DuckDuckGo

---

## 1. GitHub Repository "About" (Descripción corta)

**Texto (máx 350 caracteres):**

```
Dotfiles installer with interactive TUI for Fedora, Arch, Debian, Ubuntu & macOS. 
Automated post-install via Ansible. 100+ apps: Neovim, Tmux, Docker, Zsh, 
Homebrew. One-command setup: curl | python3
```

**Por qué funciona:**
- Keywords principales en primeros 120 chars (GitHub trunca en preview)
- Menciona plataformas (búsquedas por "fedora dotfiles", "macos setup")
- Números concretos ("100+ apps") → CTR más alto
- Call-to-action claro ("One-command setup")

---

## 2. GitHub Topics (Tags) — Máximo 20

Ordenados por prioridad de búsqueda:

```
dotfiles
ansible
fedora
archlinux
debian
ubuntu
macos
homebrew
neovim
tmux
zsh
docker
python
shell
cli
tui
setup-script
post-install
automation
linux
```

**Razonamiento:**
- **dotfiles** → Tag #1 más buscado en GitHub
- **ansible** → Diferenciador clave (la mayoría usan shell scripts)
- Distros específicas → Captura búsquedas "fedora dotfiles", "arch setup"
- **neovim, tmux, zsh** → Comunidades grandes con alta intención
- **tui** → Diferenciador único (menos repos con picker interactivo)
- **post-install** → Término de nicho pero alta conversión

---

## 3. Keywords Strategy

### Primarias (high volume, high intent)
| Keyword | Search Volume Est. | Dificultad |
|---------|-------------------|------------|
| dotfiles | 50K/mes | Alta |
| linux dotfiles | 8K/mes | Media |
| fedora post install | 2K/mes | Baja |
| arch linux setup | 5K/mes | Media |
| macos dotfiles | 3K/mes | Media |
| ansible dotfiles | 1K/mes | Baja |

### Long-tail (alta conversión)
- "fedora 41 post install script"
- "arch linux automated setup ansible"
- "macos development environment setup"
- "interactive dotfiles installer tui"
- "homebrew vs pacman dotfiles"
- "neovim tmux zsh docker setup"

### LSI (Latent Semantic Indexing)
- shell configuration, terminal setup, dev environment
- package management, system provisioning
- configuration management, infrastructure as code
- developer productivity, workflow automation

---

## 4. README.md Optimizations

### Meta Estructura

```markdown
<!-- SEO: Título H1 debe contener keyword principal -->
# SENTU Dotfiles — Automated Linux & macOS Setup

<!-- SEO: Descripción en primer párrafo, 160 chars ideal para snippet -->
> One-command post-installation framework for Fedora, Arch, Debian, Ubuntu & macOS. 
> Interactive TUI picker, 100+ apps via Ansible. Neovim, Tmux, Docker, Zsh, Homebrew.

<!-- SEO: Badges = social proof + keywords en alt text -->
[badges...]

## Características Principales (Features)
<!-- Lista con keywords naturales -->

## Instalación Rápida
<!-- Código destacado, fácil de copiar -->

## Sistemas Soportados
<!-- Tabla con keywords de distros -->

## Aplicaciones Incluidas
<!-- Inventario con categorías = más keywords -->

## Documentación
<!-- Links internos = mejor estructura -->
```

### Cambios específicos:

1. **Título H1**: "SENTU Dotfiles — Automated Linux & macOS Setup" (incluye keyword + diferenciador)
2. **Primer párrafo**: Descripción de 160 chars con keywords principales
3. **H2 headings**: Usar keywords en headings ("Instalación Rápida", "Sistemas Soportados")
4. **Alt text en imágenes**: Descriptivo con keywords
5. **Links internos**: Entre README y docs/aplicaciones.md
6. **Código fenced**: Con syntax highlighting (mejor UX = mejor SEO)
7. **Tabla de contenidos**: Facilita navegación (menor bounce rate)

---

## 5. Off-Page SEO (Acciones manuales)

### GitHub Settings (requiere acceso web):
- [ ] Website URL: https://github.com/SENTUstudio (o landing page futura)
- [ ] Topics: Agregar los 20 tags propuestos
- [ ] Social Preview: Crear imagen Open Graph (1200x630) con logo + texto

### External:
- [ ] Submit a Reddit r/linux, r/Fedora, r/archlinux, r/neovim
- [ ] Hacker News "Show HN" post
- [ ] Awesome-dotfiles PR (https://github.com/webpro/awesome-dotfiles)
- [ ] Dev.to article: "Automating my Fedora setup with Ansible"

---

## 6. Métricas a trackear

| Métrica | Herramienta | Meta (3 meses) |
|---------|-------------|----------------|
| GitHub Stars | GitHub API | +50 |
| Forks | GitHub API | +10 |
| Referrers | GitHub Insights | 5+ sources |
| Search impressions | Google Search Console | 1K/mes |
| CTR from search | GitHub Insights | >3% |

---

## 7. Notas Técnicas

### GitHub Search Ranking Factors:
1. **Relevance**: Topics, description, README content
2. **Recency**: Último commit (importa mucho)
3. **Stars**: Social proof (efecto bola de nieve)
4. **Forks**: Indica utilidad
5. **Issues/PRs**: Actividad = señal de vida

### Optimizaciones futuras:
- [ ] Crear `docs/` con más contenido (más páginas indexables)
- [ ] Blog posts en GitHub Discussions
- [ ] Releases con changelogs detallados (cada release = nuevo index)
- [ ] Wiki con guías paso a paso
