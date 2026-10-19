# awMC Client v0.3 Alpha

Lightweight personal Windows companion for the **official Minecraft Launcher**. No Azure configuration is needed.

## Features
- Open the official Minecraft Launcher (Minecraft URI handler with executable fallback)
- Dark / Light theme (saved between launches)
- Quick access to Minecraft's default `.minecraft` folder
- Shortcuts to worlds (`saves`), resource packs and mods
- Official Minecraft download website shortcut

## Download Windows EXE
1. Go to [GitHub Actions](https://github.com/alonweizzz/awMCClient/actions/workflows/build-windows.yml).
2. Open the latest **successful** Build Windows EXE run.
3. Download **awMCClient-Windows-Alpha** under Artifacts and extract `awMCClient.exe`.

## Requirements
Windows 10/11, the official Minecraft Launcher, and a Minecraft account/license to play.

## Run from source
```powershell
py app.py
```

## Limitations
This companion **opens the official launcher**, not Minecraft Java directly. Sign in, select versions (including 26.2/26.3 if available), and launch the game from the official launcher. Folder shortcuts target the default `%APPDATA%\\.minecraft` location. Mods require a compatible mod loader; opening the mods folder alone does not install one. This app is unofficial and not affiliated with Mojang/Microsoft.
