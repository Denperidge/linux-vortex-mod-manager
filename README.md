# Linux-Vortex-Mod-Manager

Vortex mod manager is annoying to set up on Linux, but the Linux options scare me. So, let's make Vortex Mod Manager less of a pain to use on Linux!

This project is made for Fallout: New Vegas on steam. But with some edits, can work with other games too.

## Explanation
### Features
- Quickly **install** and **run Vortex Mod Manager** in the **game's prefix**
- Automatically **detect** the install location for F:NV if installed in the **default Steam location**
- Displays **paths** to help **setup Vortex Mod Manager**
- If things go awry, **quickly delete** your **wine prefix**
- It does **not** support installing mods from the website as of yet

## How-to
### A) Setup requirements
1. Download [nexus.py](https://raw.githubusercontent.com/Denperidge/linux-vortex-mod-manager/refs/heads/main/nexus.py) 
```bash
wget https://raw.githubusercontent.com/Denperidge/linux-vortex-mod-manager/refs/heads/main/nexus.py
```

2. Download the vortex mod manager installer from https://www.nexusmods.com/site/mods/1?tab=files&file_id=5911
   Place it in your /home/{username}/Downloads, or in the same directory as nexus.py

### B) Game setup on Steam
1. Install Fallout: New Vegas
2. (Optional) Set compatibilitytools to Proton-GE. Proton-GE-25 was used in my Fallout: New Vegas install
3. Launch fallout, and close it once you reach the main menu

#### NVSE
If using NVSE:
1. Right-click Fallout: New Vegas in Steam
2. Select Properties
3. In the General tab, set the launch options to the line below

```bash
$(echo %command% | sed -r "s/proton waitforexitandrun .*/proton waitforexitandrun/") "$STEAM_COMPAT_INSTALL_PATH/nvse_loader.exe"
```

Thanks to [sedme0 on Reddit for that solution](https://www.reddit.com/r/linux_gaming/comments/u5wz7p/redirecting_steam_to_launch_a_different/)!


### C) Installing vortex mod manager
1. Open a console, navigate to nexus.py and either run...
```bash
python nexus.py
# or...
python3 nexus.py
# or...
chmod +x nexus.py
./nexus.py
```

2. Select Install vortex mod manager. Install it to the default location
3. After installation, run Vortex mod manager (either through nexus.py or after the vortex installer finishes)
4. Log into your nexus mods account and enable F:NV mod management
5. (Optional) If Nexus Mod Manager doesn't find the game automatically,
   navigate to the **Install path** provided by nexus.py
6. You will get a notification that mods cannot be deployed. Click Fix, and set the **mod staging folder** to the suggested directory in nexus.py.
    Optionally, you can create your own folder and navigate to it, as long as it is also on the Z: drive`
7. Install mods from file, and run the game through Steam!

## License
This project is licensed under the [MIT License](LICENSE).

