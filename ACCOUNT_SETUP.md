# Microsoft account setup

awMC Client requires a Microsoft Entra **public client** app that has permission to use the Minecraft API. New apps may require approval; this cannot be bypassed by the launcher.

1. Register an application in Microsoft Entra and configure a supported redirect URI such as `http://localhost`.
2. Follow the [minecraft-launcher-lib login guide](https://minecraft-launcher-lib.readthedocs.io/en/stable/tutorial/microsoft_login.html) to request Minecraft API permission.
3. Launch awMC Client, click **Configure Microsoft App**, and enter the Application (client) ID and exact registered redirect URI.
4. Click **Sign in with Microsoft**, sign in through the system browser, then paste the complete redirected URL into the dialog.
5. Choose a supported Minecraft release and click **Install & Play**.

The client ID is public, not a password. Never enter a Microsoft password into the launcher. Refresh tokens are stored in the Windows credential backend through Python keyring, not in the repository. An account owning Minecraft: Java Edition is required.

**Known limitation:** The redirect must be copied and pasted manually. The client does not automatically install Java. If your Entra app is not approved for Minecraft API access, authentication cannot complete.
