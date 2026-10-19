# awMC Client v0.2 Alpha

A lightweight Windows app that **opens the official Minecraft Launcher**.

## Why this approach?
No Azure app registration, custom Microsoft OAuth, credentials, or Minecraft API permissions are needed by awMC Client. **Sign in directly in the official Minecraft Launcher**, which handles the account and game installation.

## Windows EXE
1. Open the repository's **Actions → Build Windows EXE**.
2. Download the successful run's **awMCClient-Windows-Alpha** artifact.
3. Extract the ZIP and run `awMCClient.exe`.
4. Click **OPEN MINECRAFT LAUNCHER**.
5. Sign in and select the desired version **inside the official launcher**.

You must install the official Minecraft Launcher first: https://www.minecraft.net/download

## Development
Python 3.12+:
```powershell
py app.py
```

## Important limitations
- This app **does not directly start Minecraft Java**. It opens the official launcher, where you select and start the game.
- Version selection (including 26.2 and 26.3 if offered) takes place in the official launcher. awMC Client does not control or install specific versions.
- The game requires a valid license.
- This is an unofficial personal project, not affiliated with Mojang or Microsoft.
- No account passwords or tokens are collected or stored.
