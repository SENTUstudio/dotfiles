package main

import (
	"fmt"
	"os"

	"github.com/SENTUstudio/dotfiles/internal/config"
	"github.com/SENTUstudio/dotfiles/internal/dotfiles"
	"github.com/SENTUstudio/dotfiles/internal/tui"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/spf13/cobra"
)

var version = "dev"

func main() {
	cfg := config.DefaultConfig()
	engine := dotfiles.NewEngine(cfg)

	var rootCmd = &cobra.Command{
		Use:   "sentu-dotfiles",
		Short: "Gestor de dotfiles para SENTUstudio",
		Long: `sentu-dotfiles es una herramienta standalone para instalar,
actualizar y gestionar configuraciones de dotfiles.

Uso interactivo (TUI):
  sentu-dotfiles           # Lanza la interfaz interactiva

Uso por comandos (scripting):
  sentu-dotfiles deploy    # Instalar dotfiles por primera vez
  sentu-dotfiles update    # Actualizar dotfiles después de un git pull
  sentu-dotfiles status    # Ver diferencias entre repo y sistema
  sentu-dotfiles add <path> # Agregar una config del sistema al repo
  sentu-dotfiles backup    # Backup manual de configs actuales`,
		Version: version,
		Run: func(cmd *cobra.Command, args []string) {
			// Sin subcomando: lanzar TUI
			model := tui.NewModel()
			p := tea.NewProgram(model, tea.WithAltScreen())
			if _, err := p.Run(); err != nil {
				fmt.Fprintf(os.Stderr, "Error iniciando TUI: %v\n", err)
				os.Exit(1)
			}
		},
	}

	// Comando tui (explícito)
	var tuiCmd = &cobra.Command{
		Use:   "tui",
		Short: "Lanza la interfaz interactiva (TUI)",
		Run: func(cmd *cobra.Command, args []string) {
			model := tui.NewModel()
			p := tea.NewProgram(model, tea.WithAltScreen())
			if _, err := p.Run(); err != nil {
				fmt.Fprintf(os.Stderr, "Error iniciando TUI: %v\n", err)
				os.Exit(1)
			}
		},
	}

	// Comando deploy
	var deployCmd = &cobra.Command{
		Use:   "deploy",
		Short: "Instala los dotfiles por primera vez",
		Long: `Copia todos los dotfiles desde el repositorio al sistema.
Realiza backup automático de configuraciones existentes.
Elimina symlinks antiguos que apuntaban al repo sin backup.`,
		RunE: func(cmd *cobra.Command, args []string) error {
			fmt.Println("🚀 Desplegando dotfiles...")
			if err := engine.Deploy(); err != nil {
				return fmt.Errorf("❌ Error en deploy: %w", err)
			}
			fmt.Println("✅ Dotfiles desplegados exitosamente.")
			return nil
		},
	}

	// Comando update
	var updateCmd = &cobra.Command{
		Use:   "update",
		Short: "Actualiza los dotfiles (re-deploy inteligente)",
		Long: `Compara los archivos del repo con los del sistema y solo copia
los que han cambiado. Elimina archivos del sistema que ya no existen en el repo.
Realiza backup de todo lo que modifica.`,
		RunE: func(cmd *cobra.Command, args []string) error {
			fmt.Println("🔄 Actualizando dotfiles...")
			if err := engine.Update(); err != nil {
				return fmt.Errorf("❌ Error en update: %w", err)
			}
			fmt.Println("✅ Dotfiles actualizados exitosamente.")
			return nil
		},
	}

	// Comando add
	var addCmd = &cobra.Command{
		Use:   "add <path>",
		Short: "Agrega una configuración del sistema al repo",
		Long: `Copia una configuración desde ~/.config/, ~/.local/share/ o ~/
al repositorio de dotfiles. Útil para incorporar nuevas configs.`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			output, err := engine.Add(args[0])
			if err != nil {
				return err
			}
			fmt.Println(output)
			return nil
		},
	}

	// Comando status
	var statusCmd = &cobra.Command{
		Use:   "status",
		Short: "Muestra el estado de sincronización",
		Long:  `Compara los archivos del repositorio con los del sistema y muestra las diferencias.`,
		RunE: func(cmd *cobra.Command, args []string) error {
			output, err := engine.Status()
			if err != nil {
				return err
			}
			fmt.Println(output)
			return nil
		},
	}

	// Comando backup
	var backupCmd = &cobra.Command{
		Use:   "backup",
		Short: "Realiza un backup manual de las configs actuales",
		Long:  `Copia todas las configuraciones actuales del sistema al directorio de backup.`,
		RunE: func(cmd *cobra.Command, args []string) error {
			output, err := engine.Backup()
			if err != nil {
				return err
			}
			fmt.Println(output)
			return nil
		},
	}

	rootCmd.AddCommand(tuiCmd, deployCmd, updateCmd, addCmd, statusCmd, backupCmd)

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
