package tui

import (
	"github.com/charmbracelet/lipgloss"
)

var (
	// Colors
	PrimaryColor   = lipgloss.Color("#FFD700") // Gold
	SecondaryColor = lipgloss.Color("#00BFFF") // Deep Sky Blue
	SuccessColor   = lipgloss.Color("#32CD32") // Lime Green
	ErrorColor     = lipgloss.Color("#FF4500") // Orange Red
	WarningColor   = lipgloss.Color("#FFA500") // Orange
	TextColor      = lipgloss.Color("#FFFFFF") // White
	DimColor       = lipgloss.Color("#808080") // Gray
	BgColor        = lipgloss.Color("#1a1a2e") // Dark blue-black

	// Styles
	TitleStyle = lipgloss.NewStyle().
			Foreground(PrimaryColor).
			Bold(true).
			Padding(1, 2).
			Border(lipgloss.RoundedBorder()).
			BorderForeground(PrimaryColor)

	MenuStyle = lipgloss.NewStyle().
			Foreground(TextColor).
			Padding(0, 2)

	SelectedStyle = lipgloss.NewStyle().
			Foreground(SecondaryColor).
			Bold(true).
			Background(lipgloss.Color("#16213e")).
			Padding(0, 2)

	CursorStyle = lipgloss.NewStyle().
			Foreground(PrimaryColor).
			Bold(true)

	SuccessStyle = lipgloss.NewStyle().
			Foreground(SuccessColor).
			Bold(true)

	ErrorStyle = lipgloss.NewStyle().
			Foreground(ErrorColor).
			Bold(true)

	WarningStyle = lipgloss.NewStyle().
			Foreground(WarningColor)

	HelpStyle = lipgloss.NewStyle().
			Foreground(DimColor).
			Padding(1, 0)

	BoxStyle = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(SecondaryColor).
			Padding(1, 2)

	LogStyle = lipgloss.NewStyle().
			Foreground(TextColor).
			Padding(0, 2)
)
