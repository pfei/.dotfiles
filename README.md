# 🚀 dotfiles

My personal configuration files
for a productive terminal-first Linux development environment.

This repository centralizes my setup for:

- Zsh
- Tmux
- Kitty
- Helix
- Git
- Vim
- Pandoc
- themes and shell utilities

______________________________________________________________________

# 🧠 Philosophy & Design Goals

The goal is simple:

> identical workflow everywhere.

Whether on:

- a local Debian desktop,
- a remote VPS,
- a headless server,
- a temporary VM,
- or a fresh reinstall,

the experience should remain nearly identical:

- same shell,
- same terminal behavior,
- same keybindings,
- same clipboard workflow,
- same editor,
- same tmux navigation,
- same Git ergonomics.

This repository is intentionally:

- reproducible,
- idempotent,
- modular,
- portable,
- dependency-light,
- and terminal-first.

Current core stack:

- Kitty
- Tmux
- Helix
- Git
- Zsh

Everything else is optional.

______________________________________________________________________

## 🛠️ Manual Prerequisites

Before running the automation, ensure the following are installed:

### 1. System Packages & Python Build Dependencies

Essential for general workflows and compiling isolated Python environments with `pyenv`:

```bash
sudo apt update && sudo apt install -y \
curl git zsh tmux kitty xclip yad shfmt \
fonts-noto-color-emoji \
build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev libncursesw5-dev \
xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev
```

### 2. Base Frameworks

```bash
# Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

> ⚠️ The Oh My Zsh installer drops you into a temporary zsh session on completion.
> Type `exit` to return to bash, then set zsh as your default shell:
>
> ```bash
> chsh -s $(which zsh)
> ```
>
> Then **log out and log back in** — closing the terminal is not enough.
> A full session restart is required for the default shell change to take effect.

```bash
# Pyenv & plugins
curl https://pyenv.run | bash
```

> ⚠️ pyenv is not available yet in the current session after installation.
> Either open a new terminal (if zsh is already your default shell),
> or manually bootstrap it for the current session:
>
> ```bash
> export PYENV_ROOT="$HOME/.pyenv"
> export PATH="$PYENV_ROOT/bin:$PATH"
> eval "$(pyenv init -)"
> ```

```bash
# NVM (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

> ⚠️ The NVM installer will append source lines to your `.zshrc`.
> **Remove them** — NVM lazy loading is already handled in `exports.zsh`.
> After install, just reload your shell:
>
> ```bash
> omz reload
> ```

### 3. Server Configuration (Optional)

If setting up a headless environment / VPS, flag the machine as a server.

This automatically switches the shell prompt Oh My Zsh theme from:

- local desktop theme → arrow
- server theme → refined

```bash
sudo touch /etc/is_server
```

### 4. Helix Editor (AppImage)

The setup intentionally uses the official AppImage instead of distro packages.

Reason:

- distro versions are often outdated,
- AppImage guarantees consistency across machines.

Download the official AppImage: https://github.com/helix-editor/helix/releases

Then place it inside:

```bash
~/.local/bin/
```

Example:

```bash
mkdir -p ~/.local/bin
mv helix-*.AppImage ~/.local/bin/
chmod +x ~/.local/bin/helix-*.AppImage
```

The installation script automatically:

- detects the AppImage,
- creates symlinks,
- and extracts it on headless systems when FUSE is unavailable.

> 💡 **Expected shell state before running `install.py`:**
> zsh is your active default shell (verify with `echo $SHELL`),
> and pyenv responds to `pyenv --version`.
> If either is missing, revisit the steps above before continuing.

## ⚙️ Installation

Clone the repository anywhere:

```bash
git clone https://github.com/pfei/dotfiles.git ~/src/dotfiles
cd ~/src/dotfiles
git submodule update --init
./install.py
```

The installer dynamically adapts to the environment:

- desktop,
- headless VPS,
- GUI availability,
- terminal capabilities.

It automatically installs/symlinks supported modules
and skips incompatible GUI modules on headless systems.

Current modules:

- git
- zsh
- tmux
- kitty
- helix
- vim
- pandoc
- themes
- mate-terminal (legacy)

### 🐍 Post-Installation: Python Environment Integration

To complete your Python isolation setup and
make the `.zshrc` workflow fully operational,
install your target Python version
and initialize `virtualenvwrapper` hooks inside it:

For example with python 3.13.13:

```bash
# 1. Install and set your working Python version
pyenv install 3.13.13
pyenv global 3.13.13

# 2. Bind virtualenvwrapper inside the isolated version
pip install virtualenvwrapper

# 3. Reload your shell configuration
omz reload
```

### 🔒 Post-Installation: Git Identity

Git identity is loaded at install time from a local `git/identity.json` file (not tracked).
Copy the example and fill in your details:

```bash
cp git/identity.json.example git/identity.json
# then edit git/identity.json with your name, email, and SSH signing key path
```

The installer will then inject your identity into `~/.gitconfig` automatically.

______________________________________________________________________

## Features at a Glance

### 🐚 Zsh (Oh My Zsh)

A modular Zsh setup with dynamic environment handling:

- **Modular Architecture**: Configuration split into exports and functions.
- **Adaptive Themes**: Uses `refined` (e.g., `~ ❯ user@srvXXXXXX`)
  on servers via `/etc/is_server`, and `arrow` (e.g., `~ ➤`) on local machines.
- **Language Integration**: nvm, pyenv, Go, Deno — all lazy-loaded to keep shell startup fast.
- **Python Workflow**: pyenv for version management, virtualenvwrapper
  for lightweight virtual environments. Both use stub functions
  that defer initialization until first use (~500ms saved on startup).
- **Node Workflow**: nvm and its ecosystem (node, npm, npx, yarn) are lazy-loaded via stub functions.
- **Autoload Functions**: `~/.zsh_autoload_functions/` hosts private helpers
  (e.g., `load_google_api_key`) not tracked in the repository.
- **UI**: Custom steady yellow underline cursor that resets on exit.

### 🔒 Local Overrides

The `.zshrc` configuration dynamically checks for and sources `~/.zshrc.local`
right before initializing the cursor UI. This provides a clean point of extension
to inject private paths, professional/personal aliases, or specific overrides
without polluting the public repository tracking.

### 🖥️ Tmux

Terminal multiplexer configured for ergonomics and speed:

- **Prefix**: Remapped to `Ctrl-a`.
- **Navigation**: Pane switching with `Alt + Arrow Keys`,
  window switching with `Ctrl + PageUp/Down`.
- **Window Management**: Move windows left/right with `Ctrl + Shift + PageUp/Down`;
  windows auto-renumber on close; rename with `F2`.
- **Copy Mode**: vi keybindings with system clipboard integration (xclip).
  Mouse drag also copies to clipboard.
- **Clipboard**: OSC 52 passthrough enabled for seamless clipboard across SSH sessions.
- **Persistence**: New panes/windows open in the current working directory.
- **History**: 100,000 lines scrollback.

### 🐱 Kitty

- **Configuration**: `kitty/kitty.conf` → `~/.config/kitty/kitty.conf`
- `F11` mapped to toggle fullscreen.

### 💻 VS Code

- **Centralized Config**: Settings, keybindings, and snippets in one directory.
- **Automation**: One-command deployment of symlinks and extensions.
- **Smart Formatting**: Auto-format shell scripts on save via shfmt, Python via Ruff, JSON/JS/TS/HTML/CSS via Prettier.
- **Vim Integration**: Optimized Vim keybindings via vscodevim (toggle with `Ctrl+Alt+V`).
- **Spell Checking**: English and French, enabled only for Markdown files.
- **Extensions**: Ruff, Pylance, mypy, ESLint, Prettier, Jupyter, R, Rainbow CS

### 🪨 Helix

- **Configuration**: `helix/config.toml` → `~/.config/helix/config.toml`
- **Language Support**: `helix/languages.toml` → `~/.config/helix/languages.toml` — configures
  auto-formatting for Python (Ruff), Bash (shfmt), Markdown (mdformat), and JSON (jq), with debugpy integration for Python.
- **Theme**: Custom `my_mocha` theme (inherits Catppuccin Mocha with adjusted statusline colors)
  → `~/.config/helix/themes/my_mocha.toml`
- **AppImage Management**: Automatically symlinks `hx` directly to the AppImage
  on desktop environments, or extracts it cleanly into a FUSE-less standalone wrapper on headless servers.
- **Hidden Files**: `.ignore` ensures dotfiles are visible in the file picker (`Space + f`).
- **Keybindings**: `Space + n` hides line numbers, `Space + l` restores them.

### 🔧 Git

- **Configuration**: `git/gitconfig` included into `~/.gitconfig` via `[include]`
  — keeps private identity out of the repository.
- **Identity**: Loaded at install time from `git/identity.json` (not tracked).
  Copy from `git/identity.json.example`.
- **SSH Commit Signing**: Configured via `[gpg] format = ssh` with `allowed_signers`
  auto-setup. The installer appends your public key to `~/.ssh/allowed_signers` automatically.
- **Editor**: Helix (`hx`) as default commit editor.
- **Aliases**: `lg` — compact, colorized graph log with dates.
- **Jupyter Support**: `nbdime` drivers configured for notebook diff and merge.
- **Headless optimization**: On servers, `credential.helper = store` is set automatically.

### 📝 Vim

- **Configuration**: `vim/.vimrc` → `~/.vimrc`
- Relative line numbers, persistent undo, Space as leader key.
- Smart case-insensitive search, no swap/backup files.
- Clean Git commit editing (no relative numbers, no cursorline).

### 📄 Pandoc

- **Templates**: `pandoc/templates/` → `~/.local/share/pandoc/templates/`
- Clean LaTeX journal template for PDF export.

### 🎨 Themes

- **Dracula GTK**: Dracula theme submodule linked to `~/.themes/Dracula`.
- **Dracula-Yad**: Custom Dracula variant for `yad` dialogs with high-contrast cyan border and large yellow labels → `~/.themes/Dracula-Yad/`.
- **MATE Desktop**: Dracula GTK theme, Mint-Y icons, and wallpaper applied automatically via `gsettings`.
- **MATE Terminal** (legacy): Catppuccin color profiles (Mocha, Macchiato, Frappé, Latte) loaded via dconf.

______________________________________________________________________

## 🛠️ Custom Functions & Aliases

### Shell Utilities

- `h`: History search — no args shows last 20, number shows N lines, string greps.
- `lsym`: Lists symlinks in current directory with color-coded targets.
- `lst`: Shows the 5 most recently modified files.
- `dumpcode`: Dumps the full codebase to a text file for LLM analysis, skipping locks and binaries.
- `gitscan`: Scans git history for secrets using `gitleaks`. It runs in redacted mode to safely display results on public screens.

## 📂 Repository Structure

```
.
├── zsh/
│   ├── .zshrc             # Main entry point
│   ├── aliases.zsh        # Custom shortcuts
│   ├── exports.zsh        # PATH and env variables
│   ├── functions.zsh      # Utilities and helpers
│   └── setup.py           # Symlinks + autoload stub
├── tmux/
│   ├── .tmux.conf          # Tmux configuration
│   └── setup.py
├── kitty/
│   ├── kitty.conf
│   └── setup.py
├── vscode/
│   ├── settings.json
│   ├── keybindings.json
│   ├── extensions.txt
│   ├── snippets/
│   └── setup.py
├── helix/
│   ├── config.toml
│   ├── languages.toml
│   ├── themes/
│   │   └── my_mocha.toml
│   └── setup.py            # Symlinks config + hx AppImage/Wrapper
├── git/
│   ├── gitconfig
│   ├── identity.json.example
│   └── setup.py
├── vim/
│   ├── .vimrc
│   └── setup.py
├── pandoc/
│   ├── templates/          # LaTeX templates
│   └── setup.py
├── themes/
│   ├── Dracula/            # GTK theme (submodule)
│   ├── Dracula-Yad/        # Custom yad GTK theme
│   └── setup.py
├── mate-terminal/
│   ├── catppucin.dconf
│   └── setup.py
├── .local/bin/
│   └── dumpcode            # Codebase dump utility
├── install.py              # Global installer
├── .ignore                 # Show dotfiles in Helix file picker
└── LICENSE
```

______________________________________________________________________

## ⚖️ License

MIT License — see LICENSE for details.

Last updated: June 2026
