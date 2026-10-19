"""awMC Client v0.2 — opens the official Minecraft Launcher on Windows."""
import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

BG = "#101820"
PANEL = "#1d2a32"
GREEN = "#58d68d"


def launch_official_launcher():
    """Use the Windows Minecraft URI registration; fall back to installed executables."""
    if sys.platform != "win32":
        raise RuntimeError("awMC Client currently supports Windows only.")

    # Registered by the official launcher, including Microsoft Store installations.
    try:
        os.startfile("minecraft://")
        return
    except OSError:
        pass

    local = Path(os.environ.get("LOCALAPPDATA", ""))
    program_files = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
    program_files_x86 = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"))
    candidates = [
        program_files_x86 / "Minecraft Launcher" / "MinecraftLauncher.exe",
        program_files / "Minecraft Launcher" / "MinecraftLauncher.exe",
        local / "Programs" / "Minecraft Launcher" / "MinecraftLauncher.exe",
        local / "Minecraft Launcher" / "MinecraftLauncher.exe",
    ]
    for executable in candidates:
        if executable.is_file():
            subprocess.Popen([str(executable)], cwd=str(executable.parent))
            return
    raise FileNotFoundError(
        "Minecraft Launcher was not found. Install the official launcher from minecraft.net/download, "
        "sign in there, and try again."
    )


def main():
    root = tk.Tk()
    root.title("awMC Client · Alpha 0.2")
    root.geometry("520x330")
    root.resizable(False, False)
    root.configure(bg=BG)

    tk.Label(root, text="awMC Client", font=("Segoe UI", 26, "bold"),
             fg=GREEN, bg=BG).pack(pady=(28, 4))
    tk.Label(root, text="PERSONAL MINECRAFT LAUNCHER · ALPHA 0.2",
             font=("Segoe UI", 9), fg="#a2b6bb", bg=BG).pack(pady=(0, 22))
    panel = tk.Frame(root, bg=PANEL, padx=24, pady=20)
    panel.pack(fill="x", padx=34)
    status = tk.StringVar(value="Ready to open the official Minecraft Launcher")
    def open_launcher():
        try:
            launch_official_launcher()
            status.set("Official Minecraft Launcher requested")
        except Exception as exc:
            status.set("Minecraft Launcher could not be opened")
            messagebox.showerror("awMC Client", str(exc), parent=root)

    tk.Button(panel, text="OPEN MINECRAFT LAUNCHER",
              command=open_launcher, font=("Segoe UI", 13, "bold"),
              bg=GREEN, fg="#122018", relief="flat", pady=12).pack(fill="x")
    tk.Label(panel, text="Sign in and choose your game version in the official launcher.",
             bg=PANEL, fg="#d7e3e5", font=("Segoe UI", 9),
             wraplength=430).pack(pady=(14, 0))
    tk.Label(root, textvariable=status, fg="#a2b6bb", bg=BG,
             font=("Segoe UI", 9)).pack(pady=16)
    root.mainloop()


if __name__ == "__main__":
    main()
