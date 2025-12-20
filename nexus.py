#!/usr/bin/env python
from os import path, system, symlink, makedirs
from shutil import rmtree
from pathlib import Path
from urllib.request import urlretrieve

"""
TODO:
- Replace os.system
- Create suggested staging dir
- Remember input
- browser does not work natively. Circumvent using chrome exe? people menntion using xdg-open
- clear staging follder
"""


# --- CONSTANTS ---
VORTEX_DOWNLOAD_LINK = "https://github.com/Nexus-Mods/Vortex/releases/download/v1.16.0-beta.3/vortex-setup-1.16.0-beta.3.exe"
# If you're reading this in the future, get a newer version here: https://github.com/Nexus-Mods/Vortex/releases/
DEFAULT_STEAM_COMPATDATA_PATH = Path(Path.home(), ".steam/steam/steamapps/compatdata/")
DEFAULT_STEAM_APPS_PATH = Path(Path.home(), ".steam/steam/steamapps/common/")
# --- CONSTANTS: FALLOUT NEW VEGAS ---
FNV_STEAM_ID = "22380"
FNV_STEAMAPPS_NAME = "Fallout New Vegas"

# --- GENERAL TOOLING ---
def run(command):
    system(command)

def run_protontricks_in_fnv(args):
    run(f'protontricks {FNV_STEAM_ID} {args}')

def run_exe_in_prefix(exe, prefix, wine="steam-run /home/cat/.steam/steam/compatibilitytools.d/GE-Proton10-25/files/bin/wine", extra=""):
    run(f"WINEPREFIX=\"{prefix}\" STEAM_COMPAT_DATA_PATH=\"{prefix}\" STEAM_COMPAT_CLIENT_INSTALL_PATH=~/.steam/steam {wine} \"{exe}\" {extra}")

def ask_path_if_needed(title, default_path):
    if default_path.exists():
        return default_path
    else:
        while not default_path.exists():
            print(f"Could not find {title} at the expected path ({default_path})!")
            default_path = Path(input(f"Enter the {title} path: "))
        return default_path

def select(options, input_title, option_title_func=None):
    i = 0
    for option in options:
        i += 1
        title = option if option_title_func is None else option_title_func(option)
        print(f"  {i}: {title}")
    print()

    selection = "none"
    while selection != "":
        selection = input(f"{input_title}, or press ENTER to quit [1-{i}]: ")
        
        selection = int(selection)
        if selection >= 1 and selection <= i:
            break
        
    if selection == "":
        exit(0)

    if type(options) == dict:
        return options[list(options.keys())[selection-1]]
    else:
        return options[selection-1]

def remove_prefix(prefix):
    options = ["Remove", "Cancel"]
    option = select(options, f"Press 1 if you're sure you want to remove {prefix}. This is irreversible! Otherwise, press 2 to cancel")
    
    if option == options[0]:
        rmtree(prefix, True)
        if not Path(prefix).exists():
            print("Prefix removed! Launch your game again to create a new one")    


def select_mode():
    def option_title_func(mode):
        return MODES[mode]['title']

    print("Supported games:")
    return select(MODES, "Select a game to manage nexus mod manager for", option_title_func)


# --- VORTEX MOD MANAGER ---
def vortex_installer_find():
    current_dir = Path(path.dirname(path.realpath(__file__)))  # Based on the clever code at https://stackoverflow.com/a/5137509
    
    vortex_installer = []
    for location in [current_dir, Path(Path.home(), "Downloads"), Path(Path.home(), "downloads")]:
        vortex_installer += list(location.glob("Vortex*.exe")) + list(location.glob("vortex*.exe"))

    
    if len(vortex_installer) == 1:
        vortex_installer = vortex_installer[0] 
    elif len(vortex_installer) > 1:
        print("Found multiple vortex exe's. Please select one!")
        vortex_installer = select(vortex_installer, "Select your preferred vortex installer")
    else:
        print("No vortex installer found! You can either...")
        print(
            "- Cancel, manually download a release from https://github.com/Nexus-Mods/Vortex/releases/, " +
            f"put it in ~/Downloads, ~/downloads, or in the same directory as this script ({current_dir}). " +
            "Then re-run this command!")
        print(f"- Automatically download the pre-configured Vortex version in this script")
        
        VORTEX_FILENAME = VORTEX_DOWNLOAD_LINK[VORTEX_DOWNLOAD_LINK.rfind("/")+1:]
        options = [
            f"Download the pre-configured version ({VORTEX_FILENAME})",
            "Cancel"]
        selection = select(options, "Selection")
        if selection == options[0]:
            print(f"Downloading {VORTEX_FILENAME}...")
            returned_path = urlretrieve(VORTEX_DOWNLOAD_LINK, VORTEX_FILENAME)[0]
            vortex_installer = returned_path
            print("Done!")
        else:
            return None

    return vortex_installer    


def install_vortex_to_prefix(prefix):
    vortex_installer = vortex_installer_find()
    if vortex_installer == None:
        return False
    print(vortex_installer)
    run_exe_in_prefix(vortex_installer, prefix, "wine")


MODES = {
    "fnv-steam": {
        "title": "Fallout: New Vegas (Steam)",
        "default_prefix":  Path(DEFAULT_STEAM_COMPATDATA_PATH, FNV_STEAM_ID, "pfx"),
        "default_install": Path(DEFAULT_STEAM_APPS_PATH, FNV_STEAMAPPS_NAME),
        "symlink_target": "drive_c/Fallout New Vegas"
    }
}

if __name__ == "__main__":
    #mode = select_mode()  TODO: more modes
    mode = MODES["fnv-steam"]

    prefix = ask_path_if_needed("prefix", mode["default_prefix"])
    install_location = ask_path_if_needed("game install", mode["default_install"])
    suggested_staging_dir = Path(Path.home(), 'VortexMods')

    print(f"Prefix path: {prefix}")
    print(f"Install path (linux notation): {install_location}")
    print(f"Install path (windows notation): Z:{str(install_location).replace("/", "\\")}")
    print(r'NVSE Steam launch option: $(echo %command% | sed -r "s/proton waitforexitandrun .*/proton waitforexitandrun/") "$STEAM_COMPAT_INSTALL_PATH/nvse_loader.exe"')
    print(f"Suggested staging dir (linux notation): {suggested_staging_dir}")
    print(f"Suggested staging dir (windows notation): Z:{str(suggested_staging_dir).replace("/", "\\")}")
    
    print()
    actions = [
        "Install Vortex Mod Manager",
        f"Link install directory to prefix ({mode['symlink_target']})",
        f"Remove prefix ({prefix})",
        "Run Vortex Mod Manager",
        "Install .net 48",
        "Create suggested staging dir"
    ]

    action = select(actions, "Select action")
    if action == actions[0]:
        install_vortex_to_prefix(prefix)
    elif action == actions[1]:
        makedirs(Path(prefix, "drive_c/Mods"))
        symlink(
            install_location,
            Path(prefix, mode["symlink_target"]))
    elif action == actions[2]:
        remove_prefix(prefix)
    elif action == actions[3]:
        run_exe_in_prefix(
            Path(prefix, "drive_c/Program Files/Black Tree Gaming Ltd/Vortex/Vortex.exe"),
            prefix, "wine")
    elif action == actions[4]:
        #https://builds.dotnet.microsoft.com/dotnet/WindowsDesktop/6.0.36/windowsdesktop-runtime-6.0.36-win-x64.exe
        #? https://download.microsoft.com/download/f/3/a/f3a6af84-da23-40a5-8d1c-49cc10c8e76f/NDP48-x86-x64-AllOS-ENU.exe
        run_protontricks_in_fnv("dotnet48")
        #run_exe_in_prefix("dotnet48", prefix, "winetricks")
        #run_exe_in_prefix("NDP48-x86-x64-AllOS-ENU.exe", prefix, "wine")
        #run_winetricks_in_prefix(prefix, )
    elif action == actions[5]:
        makedirs(suggested_staging_dir)