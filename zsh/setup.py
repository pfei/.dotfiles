#!/usr/bin/env python3
from pathlib import Path


def main():
    print("🔗 Configuring Zsh...")

    zsh_dir = Path(__file__).resolve().parent

    # 1. Link .zshrc
    source_zshrc = zsh_dir / ".zshrc"
    target_zshrc = Path.home() / ".zshrc"

    if source_zshrc.exists():
        if target_zshrc.is_symlink() or target_zshrc.exists():
            target_zshrc.unlink()
        target_zshrc.symlink_to(source_zshrc)
        print("✅ Linked configuration: .zshrc")
    else:
        print("⚠️  No .zshrc found in dotfiles zsh directory.")
        print("   Skipping .zshrc symlink.")

    # 2. Create local folders and autoload functions
    autoload_dir = Path.home() / ".zsh_autoload_functions"
    autoload_dir.mkdir(parents=True, exist_ok=True)

    autoload_func = autoload_dir / "load_google_api_key"

    if not autoload_func.exists():
        func_content = """# Autoload function: load_google_api_key
# Loads GOOGLE_API_KEY from ~/.google_api_key (not tracked in git)
if [[ -f "$HOME/.google_api_key" ]]; then
  export GOOGLE_API_KEY="$(cat "$HOME/.google_api_key")"
else
  echo "⚠  ~/.google_api_key not found. GOOGLE_API_KEY not set."
fi
"""
        autoload_func.write_text(func_content, encoding="utf-8")
        print("✅ Created stub: ~/.zsh_autoload_functions/load_google_api_key")
    else:
        print("ℹ️  load_google_api_key already exists, skipping.")

    # 3. Check NVM installation
    nvm_dir = Path.home() / ".nvm"
    nvm_sh = nvm_dir / "nvm.sh"
    if nvm_sh.exists():
        print("✅ NVM detected: ~/.nvm/nvm.sh found.")
    else:
        print("⚠️  NVM not found at ~/.nvm")
        print(
            "   Run: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash"
        )
        print(
            "   Then remove the 3 lines it appends to ~/.zshrc — lazy loading is in exports.zsh."
        )


if __name__ == "__main__":
    main()
