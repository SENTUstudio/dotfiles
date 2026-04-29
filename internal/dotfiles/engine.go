package dotfiles

import (
	"crypto/md5"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/SENTUstudio/dotfiles/internal/config"
)

// Engine es el motor de gestión de dotfiles
type Engine struct {
	Config config.DotfilesConfig
}

// NewEngine crea una nueva instancia del engine
func NewEngine(cfg config.DotfilesConfig) *Engine {
	return &Engine{Config: cfg}
}

// Deploy realiza la instalación completa de dotfiles
// Copia todo desde el repo al sistema con backup previo
func (e *Engine) Deploy() error {
	mappings := e.Config.GetMappings()
	if len(mappings) == 0 {
		return fmt.Errorf("no se encontraron dotfiles para desplegar en %s", e.Config.DotfilesDir)
	}

	backupDir := e.backupDirWithTimestamp()

	for _, m := range mappings {
		src := filepath.Join(e.Config.DotfilesDir, m.Src)
		if _, err := os.Stat(src); os.IsNotExist(err) {
			continue
		}

		if err := e.deployItem(src, m.Dst, backupDir, m.Type); err != nil {
			return fmt.Errorf("error desplegando %s: %w", m.Src, err)
		}
	}

	return nil
}

// Update realiza un re-deploy inteligente
// Solo copia archivos que han cambiado y elimina los que ya no existen en el repo
func (e *Engine) Update() error {
	mappings := e.Config.GetMappings()
	if len(mappings) == 0 {
		return fmt.Errorf("no se encontraron dotfiles para actualizar")
	}

	backupDir := e.backupDirWithTimestamp()

	for _, m := range mappings {
		src := filepath.Join(e.Config.DotfilesDir, m.Src)
		if _, err := os.Stat(src); os.IsNotExist(err) {
			continue
		}

		if err := e.updateItem(src, m.Dst, backupDir, m.Type); err != nil {
			return fmt.Errorf("error actualizando %s: %w", m.Src, err)
		}
	}

	return nil
}

// Add incorpora una configuración del sistema al repo
func (e *Engine) Add(srcPath string) (string, error) {
	// Determinar si es config/ o home/
	home := os.Getenv("HOME")
	configDir := filepath.Join(home, ".config")
	localShareDir := filepath.Join(home, ".local", "share")

	var relSrc string

	if isSubpath(srcPath, configDir) {
		relSrc = filepath.Join("config", mustRel(configDir, srcPath))
	} else if isSubpath(srcPath, localShareDir) {
		relSrc = filepath.Join("home", "local", "share", mustRel(localShareDir, srcPath))
	} else if isSubpath(srcPath, home) {
		relSrc = filepath.Join("home", mustRel(home, srcPath))
	} else {
		return "", fmt.Errorf("la ruta %s no está en ~/.config, ~/.local/share ni ~/, no se puede determinar el destino en el repo", srcPath)
	}

	dstPath := filepath.Join(e.Config.DotfilesDir, relSrc)

	if err := os.MkdirAll(filepath.Dir(dstPath), 0755); err != nil {
		return "", fmt.Errorf("error creando directorio destino: %w", err)
	}

	if err := copyPath(srcPath, dstPath); err != nil {
		return "", fmt.Errorf("error copiando al repo: %w", err)
	}

	output := fmt.Sprintf("✅ Agregado al repo: %s -> %s\n   Recordá hacer: cd %s && git add %s && git commit", srcPath, dstPath, e.Config.DotfilesDir, relSrc)
	return output, nil
}

// Status muestra las diferencias entre repo y sistema
func (e *Engine) Status() (string, error) {
	mappings := e.Config.GetMappings()
	if len(mappings) == 0 {
		return "", fmt.Errorf("no se encontraron dotfiles")
	}

	var b strings.Builder
	b.WriteString("📊 Estado de dotfiles\n")
	b.WriteString("=====================\n")

	var differences []string
	var compareErrors []string

	for _, m := range mappings {
		src := filepath.Join(e.Config.DotfilesDir, m.Src)
		if _, err := os.Stat(src); os.IsNotExist(err) {
			continue
		}

		diffs, err := e.compareItem(src, m.Dst, m.Src)
		if err != nil {
			compareErrors = append(compareErrors, fmt.Sprintf("Error comparando %s: %v", m.Src, err))
			continue
		}
		differences = append(differences, diffs...)
	}

	if len(differences) == 0 {
		b.WriteString("\n✅ Todo sincronizado. No hay diferencias.\n")
	} else {
		b.WriteString(fmt.Sprintf("\n⚠️  Se encontraron %d diferencias:\n\n", len(differences)))
		for _, d := range differences {
			b.WriteString(d + "\n")
		}
	}

	if len(compareErrors) > 0 {
		b.WriteString(fmt.Sprintf("\n⚠️  Se encontraron %d errores de comparación:\n\n", len(compareErrors)))
		for _, e := range compareErrors {
			b.WriteString(e + "\n")
		}
	}

	return b.String(), nil
}

// Backup realiza un backup manual de las configs actuales
func (e *Engine) Backup() (string, error) {
	mappings := e.Config.GetMappings()
	if len(mappings) == 0 {
		return "", fmt.Errorf("no se encontraron dotfiles para backup")
	}

	backupDir := e.backupDirWithTimestamp()
	var backedUp []string

	for _, m := range mappings {
		if _, err := os.Stat(m.Dst); os.IsNotExist(err) {
			continue
		}

		backupPath := filepath.Join(backupDir, backupRelPath(m.Dst))
		if err := copyPath(m.Dst, backupPath); err != nil {
			return "", fmt.Errorf("error haciendo backup de %s: %w", m.Dst, err)
		}
		backedUp = append(backedUp, m.Dst)
	}

	if len(backedUp) == 0 {
		return "⚠️  No se encontraron configs para backup.", nil
	}

	output := fmt.Sprintf("✅ Backup completado en: %s\n   %d configuraciones respaldadas.", backupDir, len(backedUp))
	return output, nil
}

// --- funciones privadas ---

func (e *Engine) backupDirWithTimestamp() string {
	ts := time.Now().Format("2006-01-02_15-04-05.000")
	return filepath.Join(e.Config.BackupDir, ts)
}

func (e *Engine) deployItem(src, dst, backupDir, itemType string) error {
	// Si el destino existe
	if info, err := os.Lstat(dst); err == nil {
		// Si es un symlink nuestro (apunta a ~/dotfiles), eliminar sin backup
		if info.Mode()&os.ModeSymlink != 0 {
			linkTarget, _ := os.Readlink(dst)
			if isSubpath(linkTarget, e.Config.DotfilesDir) {
				if err := os.Remove(dst); err != nil {
					return fmt.Errorf("error eliminando symlink %s: %w", dst, err)
				}
			}
		} else {
			// Backup antes de sobrescribir
			if err := os.MkdirAll(backupDir, 0755); err != nil {
				return fmt.Errorf("error creando directorio de backup %s: %w", backupDir, err)
			}
			backupPath := filepath.Join(backupDir, backupRelPath(dst))
			if err := copyPath(dst, backupPath); err != nil {
				return fmt.Errorf("error haciendo backup de %s: %w", dst, err)
			}
			if err := os.RemoveAll(dst); err != nil {
				return fmt.Errorf("error eliminando %s: %w", dst, err)
			}
		}
	}

	return copyPath(src, dst)
}

func (e *Engine) updateItem(src, dst, backupDir, itemType string) error {
	if info, err := os.Lstat(dst); err == nil {
		if info.Mode()&os.ModeSymlink != 0 {
			linkTarget, _ := os.Readlink(dst)
			if isSubpath(linkTarget, e.Config.DotfilesDir) {
				if err := os.Remove(dst); err != nil {
					return fmt.Errorf("error eliminando symlink %s: %w", dst, err)
				}
			}
		}
	}

	if itemType == "dir" {
		return e.updateDir(src, dst, backupDir)
	}
	return e.updateFile(src, dst, backupDir)
}

func (e *Engine) updateDir(srcDir, dstDir, backupDir string) error {
	// Leer archivos en src
	srcEntries, err := os.ReadDir(srcDir)
	if err != nil {
		return err
	}

	// Crear dst si no existe
	if err := os.MkdirAll(dstDir, 0755); err != nil {
		return err
	}

	// Mapear entradas de src
	srcMap := make(map[string]bool)
	for _, entry := range srcEntries {
		srcMap[entry.Name()] = true
		srcPath := filepath.Join(srcDir, entry.Name())
		dstPath := filepath.Join(dstDir, entry.Name())

		if entry.IsDir() {
			if err := e.updateDir(srcPath, dstPath, backupDir); err != nil {
				return err
			}
		} else {
			if err := e.updateFile(srcPath, dstPath, backupDir); err != nil {
				return err
			}
		}
	}

	// Eliminar en dst lo que no está en src
	dstEntries, err := os.ReadDir(dstDir)
	if err != nil {
		return err
	}
	for _, entry := range dstEntries {
		if !srcMap[entry.Name()] {
			dstPath := filepath.Join(dstDir, entry.Name())
			// Backup antes de eliminar
			if err := os.MkdirAll(backupDir, 0755); err != nil {
				return fmt.Errorf("error creando directorio de backup %s: %w", backupDir, err)
			}
			backupPath := filepath.Join(backupDir, backupRelPath(filepath.Join(dstDir, entry.Name())))
			if err := copyPath(dstPath, backupPath); err != nil {
				return fmt.Errorf("error haciendo backup de %s: %w", dstPath, err)
			}
			if err := os.RemoveAll(dstPath); err != nil {
				return fmt.Errorf("error eliminando %s: %w", dstPath, err)
			}
		}
	}

	return nil
}

func (e *Engine) updateFile(src, dst, backupDir string) error {
	needUpdate := false

	if _, err := os.Stat(dst); os.IsNotExist(err) {
		needUpdate = true
	} else {
		same, err := filesEqual(src, dst)
		if err != nil || !same {
			needUpdate = true
		}
	}

	if needUpdate {
		if _, err := os.Stat(dst); err == nil {
			if err := os.MkdirAll(backupDir, 0755); err != nil {
				return fmt.Errorf("error creando directorio de backup %s: %w", backupDir, err)
			}
			backupPath := filepath.Join(backupDir, backupRelPath(dst))
			if err := copyPath(dst, backupPath); err != nil {
				return fmt.Errorf("error haciendo backup de %s: %w", dst, err)
			}
		}
		return copyFile(src, dst)
	}

	return nil
}

func (e *Engine) compareItem(src, dst, relPath string) ([]string, error) {
	var diffs []string

	srcInfo, err := os.Stat(src)
	if err != nil {
		return nil, err
	}

	dstInfo, err := os.Stat(dst)
	if err != nil {
		if os.IsNotExist(err) {
			diffs = append(diffs, fmt.Sprintf("❌ FALTA en sistema: %s", relPath))
			return diffs, nil
		}
		return nil, err
	}

	if srcInfo.IsDir() && dstInfo.IsDir() {
		// Comparar recursivamente
		entries, err := os.ReadDir(src)
		if err != nil {
			return nil, err
		}
		for _, entry := range entries {
			subDiffs, err := e.compareItem(
				filepath.Join(src, entry.Name()),
				filepath.Join(dst, entry.Name()),
				filepath.Join(relPath, entry.Name()),
			)
			if err != nil {
				return nil, err
			}
			diffs = append(diffs, subDiffs...)
		}
	} else if !srcInfo.IsDir() && !dstInfo.IsDir() {
		same, err := filesEqual(src, dst)
		if err != nil {
			return nil, err
		}
		if !same {
			diffs = append(diffs, fmt.Sprintf("📝 DIFERENTE: %s", relPath))
		}
	} else {
		diffs = append(diffs, fmt.Sprintf("⚠️  TIPO DIFERENTE: %s", relPath))
	}

	return diffs, nil
}

// --- utilidades ---

func copyPath(src, dst string) error {
	srcInfo, err := os.Stat(src)
	if err != nil {
		return err
	}

	if srcInfo.IsDir() {
		return copyDir(src, dst)
	}
	return copyFile(src, dst)
}

func copyDir(srcDir, dstDir string) error {
	if err := os.MkdirAll(dstDir, 0755); err != nil {
		return err
	}

	entries, err := os.ReadDir(srcDir)
	if err != nil {
		return err
	}

	for _, entry := range entries {
		srcPath := filepath.Join(srcDir, entry.Name())
		dstPath := filepath.Join(dstDir, entry.Name())

		if entry.IsDir() {
			if err := copyDir(srcPath, dstPath); err != nil {
				return err
			}
		} else {
			if err := copyFile(srcPath, dstPath); err != nil {
				return err
			}
		}
	}

	return nil
}

func copyFile(src, dst string) error {
	if err := os.MkdirAll(filepath.Dir(dst), 0755); err != nil {
		return err
	}

	srcFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer srcFile.Close()

	// Copiar a archivo temporal primero para evitar truncar dst si falla
	tmpDst := dst + ".tmp"
	dstFile, err := os.Create(tmpDst)
	if err != nil {
		return err
	}

	if _, err := io.Copy(dstFile, srcFile); err != nil {
		dstFile.Close()
		os.Remove(tmpDst)
		return err
	}

	if err := dstFile.Close(); err != nil {
		os.Remove(tmpDst)
		return err
	}

	srcInfo, err := os.Stat(src)
	if err != nil {
		os.Remove(tmpDst)
		return err
	}

	if err := os.Chmod(tmpDst, srcInfo.Mode()); err != nil {
		os.Remove(tmpDst)
		return err
	}

	// Renombrar atómicamente
	if err := os.Rename(tmpDst, dst); err != nil {
		os.Remove(tmpDst)
		return err
	}

	return nil
}

func filesEqual(a, b string) (bool, error) {
	// Comparar por tamaño primero
	aInfo, err := os.Stat(a)
	if err != nil {
		return false, err
	}
	bInfo, err := os.Stat(b)
	if err != nil {
		return false, err
	}
	if aInfo.Size() != bInfo.Size() {
		return false, nil
	}

	// Comparar por md5
	aHash, err := fileHash(a)
	if err != nil {
		return false, err
	}
	bHash, err := fileHash(b)
	if err != nil {
		return false, err
	}

	return aHash == bHash, nil
}

func fileHash(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()

	h := md5.New()
	if _, err := io.Copy(h, f); err != nil {
		return "", err
	}

	return fmt.Sprintf("%x", h.Sum(nil)), nil
}

func backupRelPath(dst string) string {
	home := os.Getenv("HOME")
	if home == "" {
		return filepath.Base(dst)
	}
	rel, err := filepath.Rel(home, dst)
	if err != nil || strings.HasPrefix(rel, "..") {
		return filepath.Base(dst)
	}
	return rel
}

func isSubpath(path, base string) bool {
	cleanPath := filepath.Clean(path)
	cleanBase := filepath.Clean(base)
	rel, err := filepath.Rel(cleanBase, cleanPath)
	if err != nil {
		return false
	}
	return rel != ".." && !filepath.IsAbs(rel) && rel != "." && !strings.HasPrefix(rel, "..")
}

func mustRel(base, target string) string {
	rel, _ := filepath.Rel(base, target)
	return rel
}
