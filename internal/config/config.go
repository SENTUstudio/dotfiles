package config

import (
	"os"
	"path/filepath"
)

// DotfilesConfig define las rutas y mapeos del sistema de dotfiles
type DotfilesConfig struct {
	DotfilesDir string
	BackupDir   string
	Mappings    []PathMapping
}

// PathMapping define un mapeo origen -> destino
type PathMapping struct {
	Src  string // relativo a DotfilesDir
	Dst  string // absoluto en el sistema
	Type string // "dir" o "file"
}

// DefaultConfig retorna la configuración por defecto
func DefaultConfig() DotfilesConfig {
	home := os.Getenv("HOME")
	if home == "" {
		home, _ = os.UserHomeDir()
	}

	dotfilesDir := filepath.Join(home, "dotfiles")

	return DotfilesConfig{
		DotfilesDir: dotfilesDir,
		BackupDir:   filepath.Join(home, ".sentu_backup"),
		Mappings: []PathMapping{
			{Src: "config", Dst: filepath.Join(home, ".config"), Type: "dir"},
			{Src: "home", Dst: home, Type: "dir"},
		},
	}
}

// GetMappingsDevuelve los mapeos expandiendo el directorio home/
func (c DotfilesConfig) GetMappings() []PathMapping {
	var expanded []PathMapping
	for _, m := range c.Mappings {
		if m.Src == "home" {
			// home/ mapea archivos/directorios individuales
			homeSrc := filepath.Join(c.DotfilesDir, "home")
			entries, err := os.ReadDir(homeSrc)
			if err != nil {
				continue
			}
			for _, entry := range entries {
				if entry.Name() == "local" {
					// home/local/share/* -> ~/.local/share/*
					localShareSrc := filepath.Join(homeSrc, "local", "share")
					shareEntries, err := os.ReadDir(localShareSrc)
					if err != nil {
						continue
					}
					for _, se := range shareEntries {
						expanded = append(expanded, PathMapping{
							Src:  filepath.Join("home", "local", "share", se.Name()),
							Dst:  filepath.Join(os.Getenv("HOME"), ".local", "share", se.Name()),
							Type: "dir",
						})
					}
					continue
				}
				expanded = append(expanded, PathMapping{
					Src:  filepath.Join("home", entry.Name()),
					Dst:  filepath.Join(c.Mappings[1].Dst, entry.Name()),
					Type: func() string {
						if entry.IsDir() {
							return "dir"
						}
						return "file"
					}(),
				})
			}
		} else if m.Src == "config" {
			// config/* -> ~/.config/*
			configSrc := filepath.Join(c.DotfilesDir, "config")
			entries, err := os.ReadDir(configSrc)
			if err != nil {
				continue
			}
			for _, entry := range entries {
				expanded = append(expanded, PathMapping{
					Src:  filepath.Join("config", entry.Name()),
					Dst:  filepath.Join(c.Mappings[0].Dst, entry.Name()),
					Type: func() string {
						if entry.IsDir() {
							return "dir"
						}
						return "file"
					}(),
				})
			}
		}
	}
	return expanded
}
