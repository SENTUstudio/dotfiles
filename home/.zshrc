# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

#  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤  Ingeniería de Datos & Data Science  ├┒
#  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤              en Python               ├┚
#              .studio en

# ▀█ █▀ █░█ █▀█ █▀▀   █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀  - @elepistemedev
# █▄ ▄█ █▀█ █▀▄ █▄▄   █▄▄ █▄█ █░▀█ █▀░ █ █▄█  - https://github.com/elepistemedev/dotfiles


if [[ -f "/opt/homebrew/bin/brew" ]] then
  # If you're using macOS, you'll want this enabled
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi
# Path
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# Set the directory we want to store zinit and plugins
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"

# Download Zinit, if it's not there yet
if [ ! -d "$ZINIT_HOME" ]; then
   mkdir -p "$(dirname $ZINIT_HOME)"
   git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
fi

# Source/Load zinit
source "${ZINIT_HOME}/zinit.zsh"

# █▀█ █░░ █░█ █▀▀ █ █▄░█ █▀
# █▀▀ █▄▄ █▄█ █▄█ █ █░▀█ ▄█

# Add in zsh plugins
zinit light zsh-users/zsh-syntax-highlighting
zinit light zsh-users/zsh-completions
zinit light zsh-users/zsh-autosuggestions
zinit light Aloxaf/fzf-tab

# Add in snippets
zinit snippet OMZL::git.zsh
zinit snippet OMZP::git
zinit snippet OMZP::sudo
zinit snippet OMZP::archlinux
zinit snippet OMZP::aws
zinit snippet OMZP::kubectl
zinit snippet OMZP::kubectx
zinit snippet OMZP::command-not-found
# zinit snippet OMZP::tmuxinator
zinit snippet OMZP::docker

# Load completions
autoload -Uz compinit && compinit

zinit cdreplay -q

# Prompt
# eval "$(oh-my-posh init zsh --config $HOME/.config/ohmyposh/negligible.omp.json)"
zinit ice depth"1"
zinit light romkatv/powerlevel10k

# Keybindings
bindkey -e
bindkey '^p' history-search-backward
bindkey '^n' history-search-forward
bindkey '^[w' kill-region

# █░█ █ █▀ ▀█▀ █▀█ █▀█ █▄█
# █▀█ █ ▄█ ░█░ █▄█ █▀▄ ░█░

# History
HISTSIZE=5000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups

# Completion styling
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'ls --color $realpath'
zstyle ':fzf-tab:complete:__zoxide_z:*' fzf-preview 'ls --color $realpath'
zstyle ':completion:*:*:docker:*' option-stacking yes
zstyle ':completion:*:*:docker-*:*' option-stacking yes

# Load completions
autoload -Uz compinit && compinit

zinit cdreplay -q

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# ▄▀█ █░░ █ ▄▀█ █▀
# █▀█ █▄▄ █ █▀█ ▄█

# Aliases
alias ls='ls --color'
alias vim='nvim'
alias c='clear'
alias ls='lsd -a --group-directories-first'
alias ll='lsd -la --group-directories-first'

alias clear='~/.config/sentu/logo.sh'

alias batfzf='bat $(fzf --preview="bat --theme=gruvbox-dark --color=always {}")'
alias nvimfzf='nvim $(fzf --preview="bat --theme=gruvbox-dark --color=always {}")'

alias yt-m='yt-dlp -x --audio-format mp3 --audio-quality 0 '

# Shell integrations
eval "$(fzf --zsh)"
eval "$(zoxide init --cmd cd zsh)"

# ▄▀█ █░█ ▀█▀ █▀█   █▀ ▀█▀ ▄▀█ █▀█ ▀█▀
# █▀█ █▄█ ░█░ █▄█   ▄█ ░█░ █▀█ █▀▄ ░█░

# NVM 
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion 

export NVM_COMPLETION=true
export NVM_SYMLINK_CURRENT="true"
zinit wait lucid light-mode for lukechilds/zsh-nvm

# Get local IP addresses
if [[ -x "$(command -v ip)" ]]; then
    alias iplocal="ip -br -c a"
else
    alias iplocal="ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"
fi

# Get public IP addresses
if [[ -x "$(command -v curl)" ]]; then
    alias ipexternal="curl -s ifconfig.me && echo"
elif [[ -x "$(command -v wget)" ]]; then
    alias ipexternal="wget -qO- ifconfig.me && echo"
fi

~/.config/sentu/logo.sh

export VISUAL=nvim
autoload edit-command-line; zle -N edit-command-line
bindkey '^X^E' edit-command-line


#d2 diagram
export PATH=$HOME/.local/bin:$PATH

# Editor en terminal
export EDITOR='nvim'

. "$HOME/.atuin/bin/env"

eval "$(atuin init zsh)"

# Cargo
export PATH="$HOME/.cargo/bin:$PATH"

# QT6 (Linux-only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  export PATH=/usr/lib64/qt6/bin:$PATH
  export QT_SELECT=6
fi

# LM Studio CLI
export PATH="$PATH:$HOME/.lmstudio/bin"

# Go
export PATH="$PATH:$HOME/go/bin"

# Ollama
export OLLAMA_NUM_THREADS=7

# Linuxbrew (descomentar si se usa en Linux)
# if [[ "$OSTYPE" == "linux-gnu"* ]]; then
#   eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
# fi

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# uv (gestor de paquetes Python) — el binario está en ~/.local/bin
# El PATH ya se configura más abajo en la sección de OpenCode

# bun completions
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# OpenCode
if [ -d "$HOME/.local/bin" ]; then
  export PATH="$HOME/.local/bin:$PATH"
fi

# Kiro CLI (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
  export PATH="$PATH:$HOME/.kiro/bin"
fi

# Cargar variables sensibles si existen
if [ -f "$HOME/.zshrc.secrets" ]; then
  source "$HOME/.zshrc.secrets"
fi

#uv Python
eval "$(uv generate-shell-completion zsh)"
eval "$(uvx --generate-shell-completion zsh)"

