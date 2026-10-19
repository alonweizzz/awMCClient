# awMC Client v0.1 (Alpha)

A lightweight **personal Minecraft: Java Edition launcher** for Windows, targeting **26.2** and **26.3**.

> This is an early prototype, not a modified Minecraft game client. It downloads official game files and launches Java Edition with a legitimate Microsoft/Minecraft account.

## Requirements
- Windows 10/11
- Python 3.10+ installed and added to PATH
- An owned Minecraft: Java Edition license
- Internet access for initial installation and login
- A Microsoft Entra application client ID approved to use the Minecraft API (see [Microsoft login documentation](https://minecraft-launcher-lib.readthedocs.io/en/stable/tutorial/microsoft_login.html))
- A compatible Java runtime (the official Minecraft Launcher may provision one; otherwise install the version required by your selected game version)

## Start
```powershell
py -m pip install -r requirements.txt
py app.py
```

Or run `start.bat` on Windows after installing Python.

## Configure Microsoft Login
1. Register a **public client** app with Microsoft Entra and configure a redirect URI (e.g. `http://localhost`), allowing public client flows as applicable.
2. Request the **Minecraft API permission**. New Azure apps need approval for Minecraft login. Follow the library's [current guide](https://minecraft-launcher-lib.readthedocs.io/en/stable/tutorial/microsoft_login.html).
3. Copy `config.example.json` to `config.json`, enter your `client_id` and `redirect_uri`.
4. Start the app, click **Sign in with Microsoft**, log in within your browser, then paste the *full redirected URL* into the launcher. The launcher verifies the OAuth state and completes the PKCE flow.
5. Select **26.2** or **26.3**, then click **Install & Play**.

No Microsoft password is typed into or stored by this program. Session data is kept in memory and you will sign in again on next launch.

## Notes
- The first game install can be large. Downloads and login occur in worker threads to keep the window responsive.
- Game files are stored in `%APPDATA%\\.awMCClient\\minecraft`, separate from your regular Minecraft installation and worlds.
- The game version must be present in Mojang's official version manifest; no unofficial builds are downloaded.
- The game uses the Java runtime available on the local machine; runtime setup is not automated in v0.1.
- There is currently no EXE build, mod loader, multiplayer enhancement, or account persistence.
- **Do not commit** `config.json` or authentication tokens.
- Minecraft is owned by Mojang/Microsoft; this is an independent, unofficial personal project.
