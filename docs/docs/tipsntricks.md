# Tips and Tricks

## Customize User Interface

At the top right of your web administration interface, click your Username > preferences. Set default tab: Servers|Workstations|Mixed

![User Preferences](images/trmm_user_preferences.png)

*****

## MeshCentral

Tactical RMM is actually 2 products: An RMM service with agent, and a secondary [MeshCentral](https://github.com/Ylianst/MeshCentral) install that handles the `Take Control` and `Remote Background` stuff.

### Adjust Settings

Right-click the connect button in *Remote Background | Terminal* for shell options

![Terminal](images/tipsntricks_meshterminal.png)

Right-click the connect button in *Take Control* for connect options

![Terminal](images/tipsntricks_meshcontrol.png)

### Enable Remote Control options

!!!note
    These settings are independant of Tactical RMM. Enable features (like auto remove inactive devices) with caution

1. Remote background a machine then go to mesh.yourdomain.com
2. Click on My Account
3. Click on the device group you want to enable notifications or accept connection etc on (probably TacticalRMM)
4. Next to User Consent click edit (the wee pencil)
5. Tick whatever boxes you want in there (Features: Sync server device name to hostname, Automatically remove inactive devices, Notify/Prompt for Consent/Connection Toolbar settings)
6. Click ok

![Features](images/mesh_features.png)

![Features](images/mesh_userconsent.png)
