#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path


def main():
    print("🔗 Configuring Helix...")

    dotfiles_dir = Path(__file__).resolve().parent
    helix_config_dir = Path.home() / ".config" / "helix"

    # 1. Handle idempotency for the config directory itself
    if helix_config_dir.is_symlink():
        helix_config_dir.unlink()
    elif helix_config_dir.exists() and not helix_config_dir.is_dir():
        helix_config_dir.unlink()

    helix_config_dir.mkdir(parents=True, exist_ok=True)

    # 2. Link configuration files (config.toml, languages.toml)
    for filename in ["config.toml", "languages.toml"]:
        source = dotfiles_dir / filename
        target = helix_config_dir / filename

        if not source.exists():
            continue

        if target.exists() or target.is_symlink():
            target.unlink()

        target.symlink_to(source)
        print(f"✅ Linked configuration: {filename}")

    # 2b. Link themes directory
    themes_source = dotfiles_dir / "themes"
    themes_target = helix_config_dir / "themes"

    if themes_source.exists():
        if themes_target.exists() or themes_target.is_symlink():
            # safe removal (dir vs file vs symlink)
            if themes_target.is_dir() and not themes_target.is_symlink():
                shutil.rmtree(themes_target)
            else:
                themes_target.unlink()

        themes_target.symlink_to(themes_source)
        print("✅ Linked Helix themes")
    else:
        print("⚠️ No themes directory found in dotfiles, skipping.")

    # 3. Handle Helix Binary / AppImage setup according to the environment
    local_bin_dir = Path.home() / ".local" / "bin"
    hx_target = local_bin_dir / "hx"

    is_headless = not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    appimages = list(local_bin_dir.glob("helix-*-x86_64.AppImage"))

    if appimages:
        target_appimage = sorted(appimages)[-1]

        if is_headless:
            print(
                "🖥️ Headless environment detected: Setting up extracted AppImage wrapper..."
            )

            dist_dir = local_bin_dir / "helix-dist"
            dist_dir.mkdir(parents=True, exist_ok=True)

            squashfs_root = dist_dir / "squashfs-root"
            if not squashfs_root.exists():
                print(f"📦 Extracting {target_appimage.name} into helix-dist...")
                subprocess.run(
                    [str(target_appimage), "--appimage-extract"],
                    cwd=str(dist_dir),
                    stdout=subprocess.DEVNULL,
                    check=True,
                )

            if hx_target.exists() or hx_target.is_symlink():
                hx_target.unlink()

            wrapper_content = f"""#!/bin/bash
export HELIX_RUNTIME="$HOME/.local/bin/helix-dist/squashfs-root/usr/lib/helix/runtime"
exec "$HOME/.local/bin/helix-dist/squashfs-root/AppRun" "$@"
"""
            hx_target.write_text(wrapper_content)
            hx_target.chmod(0o755)

            print("✅ Created and optimized Helix FUSE-less wrapper script.")

        else:
            print("💻 Desktop environment detected: Using direct AppImage symlink...")

            if hx_target.exists() or hx_target.is_symlink():
                if hx_target.is_file() and not hx_target.is_symlink():
                    print(f"⚠️ {hx_target} is a real file. Skipping symlink creation.")
                    return
                hx_target.unlink()

            hx_target.symlink_to(target_appimage)
            print(f"✅ Helix symlinked: {target_appimage.name} → hx")

    else:
        if shutil.which("hx") or hx_target.exists():
            print("✅ Helix binary (hx) or wrapper is already present.")
        else:
            print("⚠️ No Helix AppImage found in ~/.local/bin. Skipping hx setup.")

    # 4. Symlink typescript-language-server from active NVM node version
    nvm_dir = Path.home() / ".nvm"
    local_bin_dir.mkdir(parents=True, exist_ok=True)
    tsls_target = local_bin_dir / "typescript-language-server"

    if nvm_dir.exists():
        # Find the highest installed node version
        versions_dir = nvm_dir / "versions" / "node"
        node_versions = sorted(versions_dir.glob("v*")) if versions_dir.exists() else []
        if node_versions:
            active_version = node_versions[-1]
            tsls_source = active_version / "bin" / "typescript-language-server"
            if tsls_source.exists():
                if tsls_target.exists() or tsls_target.is_symlink():
                    tsls_target.unlink()
                tsls_target.symlink_to(tsls_source)
                print(f"✅ Linked typescript-language-server ({active_version.name})")
            else:
                print("⚠️  typescript-language-server not found in NVM node version.")
                print("   Run: npm install -g typescript typescript-language-server")
            # node must also be in PATH for typescript-language-server to run
            node_source = active_version / "bin" / "node"
            node_target = local_bin_dir / "node"
            if node_source.exists():
                if node_target.exists() or node_target.is_symlink():
                    node_target.unlink()
                node_target.symlink_to(node_source)
                print(f"✅ Linked node ({active_version.name})")
            else:
                print("⚠️  node binary not found in NVM version.")
        else:
            print("⚠️  NVM installed but no Node version found.")
            print("   Run: nvm install --lts && ")
            print("npm install -g typescript typescript-language-server")
    else:
        print("⚠️  NVM not found — skipping typescript-language-server symlink.")
        print("   See README: Manual Prerequisites > NVM")


if __name__ == "__main__":
    main()
