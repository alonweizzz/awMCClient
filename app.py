"""awMC Client v0.1: lightweight personal Minecraft Java launcher."""
from __future__ import annotations

import json
import os
import sys
import keyring
import subprocess
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk

import minecraft_launcher_lib as mcl

ROOT = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / ".awMCClient"
CONFIG = DATA_DIR / "config.json"
GAME_DIR = DATA_DIR / "minecraft"
VERSIONS = ("26.3", "26.2")
BG = "#101820"
PANEL = "#1d2a32"
FG = "#f2f7f5"
GREEN = "#58d68d"


def load_config() -> dict:
    if not CONFIG.exists():
        return {}
    with CONFIG.open(encoding="utf-8") as handle:
        return json.load(handle)


class Launcher:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("awMC Client · Alpha 0.1")
        self.root.geometry("570x420")
        self.root.minsize(520, 390)
        self.root.configure(bg=BG)
        self.version = tk.StringVar(value=VERSIONS[0])
        self.status = tk.StringVar(value="Ready · Sign in to play")
        self.account = None
        self.client_id = None
        self.redirect_uri = None
        self.busy = False

        tk.Label(root, text="awMC Client", font=("Segoe UI", 26, "bold"),
                 fg=GREEN, bg=BG).pack(pady=(24, 0))
        tk.Label(root, text="PERSONAL MINECRAFT JAVA LAUNCHER  •  ALPHA 0.1",
                 font=("Segoe UI", 9), fg="#a2b6bb", bg=BG).pack(pady=(0, 20))

        panel = tk.Frame(root, bg=PANEL, padx=28, pady=20)
        panel.pack(fill="x", padx=35)
        tk.Label(panel, text="GAME VERSION", font=("Segoe UI", 10, "bold"),
                 fg=FG, bg=PANEL).pack(anchor="w")
        version_choice = ttk.Combobox(panel, textvariable=self.version, values=VERSIONS,
                                      state="readonly", width=18)
        version_choice.pack(anchor="w", pady=(6, 18))
        self.login_button = tk.Button(panel, text="Sign in with Microsoft",
                                      command=self.login, font=("Segoe UI", 11),
                                      bg="#354c59", fg="white", relief="flat", padx=15, pady=7)
        self.login_button.pack(fill="x")
        tk.Button(panel, text="Configure Microsoft App", command=self.configure, bg="#354c59", fg="white", relief="flat").pack(fill="x", pady=(6, 0))
        self.play_button = tk.Button(panel, text="INSTALL & PLAY", command=self.play,
                                     font=("Segoe UI", 13, "bold"), bg=GREEN, fg="#122018",
                                     relief="flat", padx=15, pady=10, state="disabled")
        self.play_button.pack(fill="x", pady=(10, 0))

        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.pack(fill="x", padx=35, pady=(18, 5))
        tk.Label(root, textvariable=self.status, font=("Segoe UI", 10),
                 fg=FG, bg=BG, wraplength=500).pack(pady=4)
        tk.Label(root, text="Official game files • Microsoft account required",
                 fg="#8fa4ac", bg=BG, font=("Segoe UI", 9)).pack(side="bottom", pady=16)

    def set_status(self, message: str):
        self.root.after(0, self.status.set, message)

    def set_busy(self, busy: bool):
        self.busy = busy
        def update():
            self.login_button.config(state="disabled" if busy else "normal")
            self.play_button.config(state="normal" if self.account and not busy else "disabled")
            self.progress.start(10) if busy else self.progress.stop()
        self.root.after(0, update)

    def fail(self, title: str, exc: Exception):
        self.set_status(f"Error: {exc}")
        self.root.after(0, lambda: messagebox.showerror(title, str(exc)))

    def run_worker(self, function):
        if self.busy:
            return
        self.set_busy(True)
        def worker():
            try:
                function()
            except Exception as exc:
                self.fail("awMC Client", exc)
            finally:
                self.set_busy(False)
        threading.Thread(target=worker, daemon=True).start()

    def login(self):
        config = load_config()
        if not config.get("client_id", "").strip() or config.get("client_id", "").startswith("PASTE_") or not config.get("redirect_uri", "").strip():
            self.status.set("Configure your Microsoft application first.")
            messagebox.showinfo("Microsoft setup", "To sign in, enter a Microsoft application Client ID with Minecraft API access. The next window will save these settings.")
            self.configure()
            return
        def task():
            config = load_config()
            client_id = config.get("client_id", "").strip()
            redirect = config.get("redirect_uri", "").strip()
            if not client_id or client_id.startswith("PASTE_") or not redirect:
                raise ValueError("Microsoft app configuration is missing. Use Configure Microsoft App.")
            url, state, verifier = mcl.microsoft_account.get_secure_login_data(client_id, redirect)
            self.set_status("Browser opened. Sign in and paste the complete redirected URL.")
            webbrowser.open(url)
            # Tk input dialogs must run on the GUI thread.
            answer = {}
            event = threading.Event()
            def ask():
                from tkinter import simpledialog
                answer["value"] = simpledialog.askstring(
                    "Microsoft sign-in",
                    "After signing in, copy the COMPLETE URL in your browser's address bar and paste it here:",
                    parent=self.root,
                )
                event.set()
            self.root.after(0, ask)
            event.wait()
            returned_url = answer.get("value")
            if not returned_url:
                self.set_status("Sign-in cancelled")
                return
            code = mcl.microsoft_account.parse_auth_code_url(returned_url, state)
            # Explicit redirect_uri keyword to avoid signature ambiguity.
            data = mcl.microsoft_account.complete_login(
                client_id, None, redirect, code, verifier
            )
            self.client_id, self.redirect_uri = client_id, redirect
            if data.get("refresh_token"):
                keyring.set_password("awMCClient", client_id, data["refresh_token"])
            self.account = {
                "username": data["name"],
                "uuid": data["id"],
                "token": data["access_token"],
            }
            self.set_status("Signed in as " + data["name"])
        self.run_worker(task)

    def configure(self):
        from tkinter import simpledialog
        config = load_config()
        cid = simpledialog.askstring("Microsoft App", "Application (client) ID:", initialvalue=config.get("client_id", ""), parent=self.root)
        if cid is None:
            return
        redirect = simpledialog.askstring("Microsoft App", "Registered redirect URI:", initialvalue=config.get("redirect_uri", "http://localhost"), parent=self.root)
        if redirect is None:
            return
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG.write_text(json.dumps({"client_id": cid.strip(), "redirect_uri": redirect.strip()}, indent=2), encoding="utf-8")
        self.status.set("Microsoft app settings saved. You can sign in now.")

    def play(self):
        def task():
            version = self.version.get()
            config = load_config()
            cid, redirect = config.get("client_id", ""), config.get("redirect_uri", "")
            refresh = keyring.get_password("awMCClient", cid) if cid else None
            if refresh:
                try:
                    fresh = mcl.microsoft_account.complete_refresh(cid, None, redirect, refresh)
                    self.account = {"username": fresh["name"], "uuid": fresh["id"], "token": fresh["access_token"]}
                    if fresh.get("refresh_token"):
                        keyring.set_password("awMCClient", cid, fresh["refresh_token"])
                except Exception:
                    self.set_status("Session refresh failed. Sign in again.")
                    raise ValueError("Microsoft session expired. Please sign in again.")
            if version not in VERSIONS:
                raise ValueError("Unsupported version")
            self.set_status(f"Checking official Mojang manifest for {version}...")
            available = {
                v["id"] for v in mcl.utils.get_version_list()
                if v.get("type") == "release"
            }
            if version not in available:
                raise ValueError(f"Version {version} is not in Mojang's release manifest.")
            GAME_DIR.mkdir(parents=True, exist_ok=True)
            self.set_status(f"Installing Minecraft {version} (first run may take a while)...")
            mcl.install.install_minecraft_version(version, str(GAME_DIR))
            self.set_status(f"Starting Minecraft {version}...")
            command = mcl.command.get_minecraft_command(
                version, str(GAME_DIR), dict(self.account)
            )
            subprocess.Popen(command, cwd=str(GAME_DIR))
            self.set_status(f"Minecraft {version} launched!")
        self.run_worker(task)


if __name__ == "__main__":
    window = tk.Tk()
    Launcher(window)
    window.mainloop()
