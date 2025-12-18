#!/usr/bin/env python
from os import path, system, symlink, makedirs
from shutil import rmtree
from pathlib import Path


"""
TODO:
- Replace os.system
- Create suggested staging dir
- Remember input
- browser does not work natively. Circumvent using chrome exe?

"""


# --- CONSTANTS ---
DEFAULT_STEAM_COMPATDATA_PATH = Path(Path.home(), ".steam/steam/steamapps/compatdata/")
DEFAULT_STEAM_APPS_PATH = Path(Path.home(), ".steam/steam/steamapps/common/")
# --- CONSTANTS: FALLOUT NEW VEGAS ---
FNV_STEAM_ID = "22380"
FNV_STEAMAPPS_NAME = "Fallout New Vegas"

# --- GENERAL TOOLING ---
def run(command):
    system(command)

def run_protontricks_in_prefix(prefix, args):
    run(f'protontricks {args}')

def run_exe_in_prefix(exe, prefix, wine="steam-run /home/cat/.steam/steam/compatibilitytools.d/GE-Proton10-25/files/bin/wine"):
    run(f"WINEPREFIX=\"{prefix}\" STEAM_COMPAT_DATA_PATH=\"{prefix}\" STEAM_COMPAT_CLIENT_INSTALL_PATH=~/.steam/steam {wine} \"{exe}\"")

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
        vortex_installer += list(location.glob("Vortex*.exe"))

    if len(vortex_installer) == 0:
        raise FileNotFoundError(
            "Could not find Vortex mod manager exe!" +
            "\nDue to Nexus Mods limitations, you have to get it yourself. Sorry boss" +
            "\n1. Download it from: https://www.nexusmods.com/site/mods/1?tab=files&file_id=5911" +
            f"\n2. And put it in ~/Downloads, ~/downloads, or in the same directory as this script: {current_dir}")
    elif len(vortex_installer) > 1:
        print("Found multiple vortex exe's. Please select one!")
        vortex_installer = select(vortex_installer, "Select your preferred vortex installer")
    else:
        vortex_installer = vortex_installer[0]
    return vortex_installer    


def install_vortex_to_prefix(prefix):
    vortex_installer = vortex_installer_find()
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
        "Install .net 6",
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
        run_exe_in_prefix("windowsdesktop-runtime-6.0.36-win-x64.exe", prefix, "wine")
        #run_winetricks_in_prefix(prefix, )
    elif action == actions[5]:
        makedirs(suggested_staging_dir)