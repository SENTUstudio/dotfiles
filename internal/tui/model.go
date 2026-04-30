package tui

import (
	"fmt"
	"strings"
	"unicode/utf8"

	"github.com/SENTUstudio/dotfiles/internal/config"
	"github.com/SENTUstudio/dotfiles/internal/dotfiles"
	"github.com/SENTUstudio/dotfiles/internal/setup"
	"github.com/charmbracelet/bubbles/spinner"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// screen representa la pantalla actual
type screen int

const (
	screenMenu screen = iota
	screenExecuting
	screenResult
	screenAddInput
)

// menuItem representa una opción del menú
type menuItem struct {
	title       string
	description string
	action      string
}

var menuItems = []menuItem{
	{title: "⚙️  Setup", description: "Instalar apps y configurar sistema", action: "setup"},
	{title: "🚀 Deploy", description: "Instalar dotfiles por primera vez", action: "deploy"},
	{title: "🔄 Update", description: "Actualizar dotfiles (solo cambios)", action: "update"},
	{title: "📊 Status", description: "Ver diferencias entre repo y sistema", action: "status"},
	{title: "➕ Add", description: "Agregar una config del sistema al repo", action: "add"},
	{title: "💾 Backup", description: "Backup manual de configs actuales", action: "backup"},
	{title: "❌ Salir", description: "Salir de sentu-dotfiles", action: "exit"},
}

// Model es el modelo de la TUI
type Model struct {
	screen      screen
	cursor      int
	engine      *dotfiles.Engine
	width       int
	height      int
	spinner     spinner.Model
	executing   bool
	action      string
	result      string
	resultError bool
	addPath     string
	logs        []string
}

// NewModel crea un nuevo modelo de TUI
func NewModel() Model {
	s := spinner.New()
	s.Spinner = spinner.Dot
	s.Style = lipgloss.NewStyle().Foreground(SecondaryColor)

	cfg := config.DefaultConfig()
	return Model{
		screen:  screenMenu,
		cursor:  0,
		engine:  dotfiles.NewEngine(cfg),
		spinner: s,
		logs:    make([]string, 0),
	}
}

// Init implementa tea.Model
func (m Model) Init() tea.Cmd {
	return nil
}

// Update implementa tea.Model
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch m.screen {
		case screenMenu:
			return m.updateMenu(msg)
		case screenResult:
			return m.updateResult(msg)
		case screenAddInput:
			return m.updateAddInput(msg)
		case screenExecuting:
			if msg.String() == "ctrl+c" {
				return m, tea.Quit
			}
		}

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		return m, nil

	case execDoneMsg:
		m.executing = false
		m.screen = screenResult
		if msg.err != nil {
			m.result = msg.err.Error()
			m.resultError = true
		} else {
			m.result = msg.output
			m.resultError = false
		}
		return m, nil
	}

	if m.executing {
		var cmd tea.Cmd
		m.spinner, cmd = m.spinner.Update(msg)
		return m, cmd
	}

	return m, nil
}

func (m Model) updateMenu(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch msg.String() {
	case "q", "ctrl+c":
		return m, tea.Quit
	case "up", "k":
		if m.cursor > 0 {
			m.cursor--
		}
	case "down", "j":
		if m.cursor < len(menuItems)-1 {
			m.cursor++
		}
	case "enter":
		item := menuItems[m.cursor]
		if item.action == "exit" {
			return m, tea.Quit
		}
		if item.action == "add" {
			m.screen = screenAddInput
			m.addPath = ""
			return m, nil
		}
		m.action = item.action
		m.executing = true
		m.screen = screenExecuting
		return m, tea.Batch(
			m.spinner.Tick,
			m.executeAction(item.action),
		)
	}
	return m, nil
}

func (m Model) updateResult(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch msg.String() {
	case "q", "ctrl+c", "esc", "enter":
		m.screen = screenMenu
		m.result = ""
		m.resultError = false
	}
	return m, nil
}

func (m Model) updateAddInput(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch msg.String() {
	case "esc":
		m.screen = screenMenu
		m.addPath = ""
		return m, nil
	case "ctrl+c":
		return m, tea.Quit
	case "enter":
		if m.addPath != "" {
			m.action = "add"
			m.executing = true
			m.screen = screenExecuting
			return m, tea.Batch(
				m.spinner.Tick,
				m.executeAdd(m.addPath),
			)
		}
	case "backspace":
		if len(m.addPath) > 0 {
			// Truncar por runes para manejar UTF-8 correctamente
			runes := []rune(m.addPath)
			if len(runes) > 0 {
				m.addPath = string(runes[:len(runes)-1])
			}
		}
	default:
		// Aceptar caracteres printables (incluyendo UTF-8 multibyte)
		if utf8.RuneCountInString(msg.String()) == 1 && msg.Type == tea.KeyRunes {
			m.addPath += msg.String()
		}
	}
	return m, nil
}

// View implementa tea.Model
func (m Model) View() string {
	switch m.screen {
	case screenMenu:
		return m.viewMenu()
	case screenExecuting:
		return m.viewExecuting()
	case screenResult:
		return m.viewResult()
	case screenAddInput:
		return m.viewAddInput()
	}
	return ""
}

func (m Model) viewMenu() string {
	var b strings.Builder

	// Logo
	logo := `
  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤ Ingeniería de Datos & Data Science ├┒
  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤  Dotfiles Manager                  ├┚
                .studio`
	b.WriteString(TitleStyle.Render(logo))
	b.WriteString("\n\n")

	// Menu
	b.WriteString(MenuStyle.Render("Seleccioná una opción:"))
	b.WriteString("\n\n")

	for i, item := range menuItems {
		cursor := "  "
		if m.cursor == i {
			cursor = CursorStyle.Render("> ")
			line := SelectedStyle.Render(fmt.Sprintf("%-12s %s", item.title, DimStyle.Render(item.description)))
			b.WriteString(cursor + line + "\n")
		} else {
			line := MenuStyle.Render(fmt.Sprintf("%-12s %s", item.title, DimStyle.Render(item.description)))
			b.WriteString(cursor + line + "\n")
		}
	}

	b.WriteString("\n")
	b.WriteString(HelpStyle.Render("↑/k ↓/j navegar • enter seleccionar • q salir"))

	return b.String()
}

func (m Model) viewExecuting() string {
	var b strings.Builder
	b.WriteString(TitleStyle.Render("sentu-dotfiles"))
	b.WriteString("\n\n")

	actionNames := map[string]string{
		"setup":  "Instalando apps y configurando sistema",
		"deploy": "Desplegando dotfiles",
		"update": "Actualizando dotfiles",
		"status": "Verificando estado",
		"add":    "Agregando configuración",
		"backup": "Realizando backup",
	}

	actionName := actionNames[m.action]
	if actionName == "" {
		actionName = "Ejecutando"
	}

	b.WriteString(fmt.Sprintf("%s %s...\n", m.spinner.View(), actionName))
	b.WriteString("\n")
	b.WriteString(HelpStyle.Render("Esperá un momento..."))

	return b.String()
}

func (m Model) viewResult() string {
	var b strings.Builder
	b.WriteString(TitleStyle.Render("sentu-dotfiles"))
	b.WriteString("\n\n")

	if m.resultError {
		b.WriteString(ErrorStyle.Render("❌ Error") + "\n\n")
		b.WriteString(BoxStyle.Render(m.result))
	} else {
		b.WriteString(SuccessStyle.Render("✅ Completado") + "\n\n")
		if m.result != "" {
			b.WriteString(BoxStyle.Render(m.result))
		} else {
			b.WriteString(BoxStyle.Render("Operación completada exitosamente."))
		}
	}

	b.WriteString("\n")
	b.WriteString(HelpStyle.Render("enter/esc para volver al menú"))

	return b.String()
}

func (m Model) viewAddInput() string {
	var b strings.Builder
	b.WriteString(TitleStyle.Render("sentu-dotfiles"))
	b.WriteString("\n\n")
	b.WriteString(MenuStyle.Render("Agregar configuración al repo"))
	b.WriteString("\n\n")
	b.WriteString("Ingresá la ruta de la configuración:\n")
	b.WriteString(BoxStyle.Render(m.addPath + "█"))
	b.WriteString("\n\n")
	b.WriteString(HelpStyle.Render("enter confirmar • esc cancelar"))
	return b.String()
}

// execDoneMsg se envía cuando termina una ejecución
type execDoneMsg struct {
	output string
	err    error
}

// DimStyle es un estilo para texto atenuado
var DimStyle = lipgloss.NewStyle().Foreground(DimColor)

func (m Model) executeAction(action string) tea.Cmd {
	return func() tea.Msg {
		var err error
		var output string
		switch action {
		case "deploy":
			err = m.engine.Deploy()
		case "update":
			err = m.engine.Update()
		case "status":
			output, err = m.engine.Status()
			if err != nil {
				return execDoneMsg{err: err}
			}
			return execDoneMsg{output: output}
		case "backup":
			output, err = m.engine.Backup()
			if err != nil {
				return execDoneMsg{err: err}
			}
			return execDoneMsg{output: output}
		case "setup":
			runner := setup.NewRunner(m.engine.Config.DotfilesDir)
			if err := runner.Run(); err != nil {
				return execDoneMsg{err: err}
			}
			if err := m.engine.Deploy(); err != nil {
				return execDoneMsg{err: err}
			}
			return execDoneMsg{output: "Setup y deploy completados exitosamente."}
		default:
			return execDoneMsg{err: fmt.Errorf("acción desconocida: %s", action)}
		}

		if err != nil {
			return execDoneMsg{err: err}
		}
		return execDoneMsg{output: "Operación completada exitosamente."}
	}
}

func (m Model) executeAdd(path string) tea.Cmd {
	return func() tea.Msg {
		output, err := m.engine.Add(path)
		if err != nil {
			return execDoneMsg{err: err}
		}
		return execDoneMsg{output: output}
	}
}
