// Package setup orquesta la instalación completa del sistema delegando a Python/Ansible.
package setup

import (
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strings"
)

// Runner ejecuta el setup completo del sistema vía sentu_install.py.
type Runner struct {
	DotfilesDir string
}

// NewRunner crea un nuevo runner apuntando al directorio de dotfiles.
func NewRunner(dotfilesDir string) *Runner {
	return &Runner{DotfilesDir: dotfilesDir}
}

// detectOSFamily determina la familia del SO para las variables de Ansible.
func detectOSFamily() (string, error) {
	switch runtime.GOOS {
	case "darwin":
		return "Darwin", nil
	case "linux":
		// Leer /etc/os-release para detectar la distro
		data, err := os.ReadFile("/etc/os-release")
		if err != nil {
			return "", fmt.Errorf("no se pudo detectar la distro Linux: %w", err)
		}
		content := string(data)
		for _, line := range strings.Split(content, "\n") {
			if strings.HasPrefix(line, "ID=") {
				distro := strings.Trim(strings.SplitN(line, "=", 2)[1], `"`)
				switch distro {
				case "fedora", "rhel", "centos", "rocky", "almalinux":
					return "RedHat", nil
				case "arch":
					return "Archlinux", nil
				case "debian", "ubuntu", "pop", "mint":
					return "Debian", nil
				default:
					return "", fmt.Errorf("distro Linux no soportada: %s", distro)
				}
			}
		}
		return "", fmt.Errorf("no se encontró ID en /etc/os-release")
	default:
		return "", fmt.Errorf("sistema operativo no soportado: %s", runtime.GOOS)
	}
}

// python3Command busca el ejecutable de Python 3.
func python3Command() (string, error) {
	candidates := []string{"python3", "python"}
	for _, cmd := range candidates {
		if path, err := exec.LookPath(cmd); err == nil {
			// Verificar que sea Python 3
			out, err := exec.Command(path, "--version").Output()
			if err == nil && strings.HasPrefix(string(out), "Python 3") {
				return path, nil
			}
		}
	}
	return "", fmt.Errorf("Python 3 no está instalado. Instalalo manualmente")
}

// Run ejecuta el setup completo.
// 1. Detecta OS family
// 2. Verifica Python3
// 3. Ejecuta sentu_install.py --setup-only
// 4. Si Python termina exit 0, retorna nil
func (r *Runner) Run() error {
	osFamily, err := detectOSFamily()
	if err != nil {
		return err
	}

	python, err := python3Command()
	if err != nil {
		return err
	}

	installerPath := fmt.Sprintf("%s/sentu_install.py", r.DotfilesDir)
	if _, err := os.Stat(installerPath); os.IsNotExist(err) {
		return fmt.Errorf("no se encontró el instalador Python en %s", installerPath)
	}

	fmt.Println("⚙️  Iniciando instalación completa del sistema...")
	fmt.Printf("   OS Family: %s\n", osFamily)
	fmt.Println("   Delegando a sentu_install.py (Python)...")
	fmt.Println()

	cmd := exec.Command(python, installerPath, "--setup-only")
	cmd.Dir = r.DotfilesDir
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("el setup falló: %w", err)
	}

	fmt.Println()
	fmt.Println("✅ Setup completado.")
	return nil
}
