# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time Oh My Zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes

# different theme for server (create the empty `/etc/is_server` file first)
if [[ -f /etc/is_server ]]; then
    ZSH_THEME="refined"
else
    ZSH_THEME="minimal"
fi


# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='nvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch $(uname -m)"

# Set personal aliases, overriding those provided by Oh My Zsh libs,
# plugins, and themes. Aliases can be placed here, though Oh My Zsh
# users are encouraged to define aliases within a top-level file in
# the $ZSH_CUSTOM folder, with .zsh extension. Examples:
# - $ZSH_CUSTOM/aliases.zsh
# - $ZSH_CUSTOM/macos.zsh
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"


function h() {
    local default_lines=20

    if [[ $# -eq 0 ]]; then
        # If no arguments, show last $default_lines entries
        fc -l -$default_lines
    elif [[ "$1" =~ ^-?[0-9]+$ ]]; then
        # If first argument is a number, show that many lines
        fc -l -${1#-}
    else
        # Otherwise, search history
        fc -l 1 | grep --color=auto -i "$@"
    fi
}

function tmux_run_and_notify() {
  local initial_status=$(tmux show-option -gv status-right)
  local start_time=$(date +%s)

  # Run the command and capture its output
  local command_output
  command_output=$("$@")
  local command_exit_status=$?

  # Calculate duration
  local end_time=$(date +%s)
  local duration=$((end_time - start_time))

  # Update status bar with completion message
  tmux set-option -g status-right \
  "#[fg=yellow,bold]Command completed in ${duration}s at $(date +%H:%M:%S)#[default]"

  # Return the initial status (this will be captured by the caller)
  echo "$initial_status"

  return $command_exit_status
}
alias trn='tmux_run_and_notify'

# $ tmux_restore_status "$saved_status"
function tmux_restore_status() {
  if [[ -n "$1" ]]; then
    tmux set-option -g status-right "$1"
    echo "Tmux status-right restored."
  else
    echo "Error: No status provided to restore."
  fi
}
alias trs='tmux_restore_status'

function lsym() {
    local maxdepth=${1:-1} # first argument if provided, otherwise defaults to 1
    find . -maxdepth $maxdepth -type l -printf '%p -> %l\n' | while read line; do
        symlink=$(echo "$line" | cut -d' ' -f1)
        target=$(echo "$line" | cut -d' ' -f3-)
        echo -e "\033[36m$symlink\033[0m -> $target"
    done
}


export TMUX_TIME_FORMAT="| %H:%M |"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
