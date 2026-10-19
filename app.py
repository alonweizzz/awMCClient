"""awMC Client v0.3 — simple Windows companion for the official Minecraft Launcher."""
import json
import os
import subprocess
import sys
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk

APP_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / ".awMCClient"
SETTINGS = APP_DIR / "settings.json"
MC_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / ".minecraft"
DARK = {"bg": "#101820", "panel": "#1d2a32", "fg": "#f2f7f5", "muted": "#a2b6bb", "accent": "#58d68d"}
LIGHT = {"bg": "#eef3f1", "panel": "#ffffff", "fg": "#162a26", "muted": "#526a65", "accent": "#218b54"}


def open_launcher():
    """Find the installed launcher without invoking an unregistered minecraft:// URI."""
    if sys.platform != "win32":
        raise RuntimeError("Windows is required.")
    local = Path(os.environ.get("LOCALAPPDATA", str(Path.home())))
    pf = Path(os.environ.get("ProgramFiles", r"C:\\Program Files"))
    pf86 = Path(os.environ.get("ProgramFiles(x86)", r"C:\\Program Files (x86)"))
    candidates = [
        pf86 / "Minecraft Launcher" / "MinecraftLauncher.exe",
        pf / "Minecraft Launcher" / "MinecraftLauncher.exe",
        local / "Programs" / "Minecraft Launcher" / "MinecraftLauncher.exe",
        local / "Minecraft Launcher" / "MinecraftLauncher.exe",
        local / "Microsoft" / "WindowsApps" / "MinecraftLauncher.exe",
    ]
    for path in candidates:
        if path.is_file():
            subprocess.Popen([str(path)], cwd=str(path.parent))
            return
    # Windows Store installations may register an AppUserModelID instead of an exe path.
    # Try the official Store app activation, which doesn't require the minecraft:// protocol.
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
             "$app = Get-StartApps | Where-Object { $_.Name -eq 'Minecraft Launcher' } | Select-Object -First 1; "
             "if ($app) { Start-Process explorer.exe ('shell:AppsFolder\\' + $app.AppID) } "
             "else { exit 2 }"],
            capture_output=True, text=True, timeout=15, check=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode == 0:
            return
    except (OSError, subprocess.TimeoutExpired):
        pass
    raise FileNotFoundError(
        "Minecraft Launcher was not found. Install the official Minecraft Launcher "
        "from https://www.minecraft.net/download, then try again."
    )


def open_folder(path):
    if sys.platform != "win32":
        raise RuntimeError("Windows is required.")
    path.mkdir(parents=True, exist_ok=True)
    os.startfile(str(path))


def read_settings():
    try:
        return json.loads(SETTINGS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def main():
    settings = read_settings()
    root = tk.Tk()
    root.title("awMC Client · Alpha 0.3")
    root.geometry("640x530")
    root.minsize(570, 500)
    theme = tk.StringVar(value=settings.get("theme", "Dark"))
    status = tk.StringVar(value="Ready · Official Minecraft Launcher mode")
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    def safe_run(callback):
        try:
            callback()
            status.set("Action completed")
        except Exception as exc:
            status.set("Action failed")
            messagebox.showerror("awMC Client", str(exc), parent=root)

    def save_settings(*_):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        SETTINGS.write_text(json.dumps({"theme": theme.get()}, indent=2), encoding="utf-8")
        render()

    def render():
        colors = DARK if theme.get() == "Dark" else LIGHT
        root.configure(bg=colors["bg"])
        for child in container.winfo_children():
            child.destroy()
        container.configure(bg=colors["bg"])
        tk.Label(container, text="awMC Client", font=("Segoe UI", 28, "bold"),
                 bg=colors["bg"], fg=colors["accent"]).pack(pady=(24, 2))
        tk.Label(container, text="MINECRAFT COMPANION  ·  ALPHA 0.3",
                 font=("Segoe UI", 10), bg=colors["bg"], fg=colors["muted"]).pack(pady=(0, 20))
        panel = tk.Frame(container, bg=colors["panel"], padx=24, pady=18)
        panel.pack(fill="x", padx=35)

        def action(label, callback, primary=False):
            tk.Button(panel, text=label, command=lambda: safe_run(callback),
                      font=("Segoe UI", 11, "bold" if primary else "normal"),
                      bg=colors["accent"] if primary else colors["bg"],
                      fg="#ffffff" if primary and theme.get() == "Light" else
                         "#102019" if primary else colors["fg"],
                      relief="flat", pady=10).pack(fill="x", pady=4)

        action("▶  OPEN MINECRAFT LAUNCHER", open_launcher, True)
        action("📁  Open Minecraft Folder", lambda: open_folder(MC_DIR))
        action("🌍  Open Saves / Worlds", lambda: open_folder(MC_DIR / "saves"))
        action("📦  Open Resource Packs", lambda: open_folder(MC_DIR / "resourcepacks"))
        action("🧩  Open Mods Folder", lambda: open_folder(MC_DIR / "mods"))
        footer = tk.Frame(container, bg=colors["bg"])
        footer.pack(fill="x", padx=35, pady=(15, 0))
        tk.Label(footer, text="Theme", bg=colors["bg"], fg=colors["fg"]).pack(side="left")
        ttk.Combobox(footer, values=("Dark", "Light"), textvariable=theme,
                     state="readonly", width=12).pack(side="left", padx=12)
        tk.Button(footer, text="Minecraft website",
                  command=lambda: webbrowser.open("https://www.minecraft.net/download"),
                  relief="flat").pack(side="right")
        tk.Label(container, textvariable=status, bg=colors["bg"], fg=colors["muted"],
                 font=("Segoe UI", 9)).pack(pady=12)
        tk.Label(container, text="Sign in and select your version in the official launcher.",
                 bg=colors["bg"], fg=colors["muted"]).pack(side="bottom", pady=8)

    theme.trace_add("write", save_settings)
    render()
    root.mainloop()


if __name__ == "__main__":
    main()
