from os import path
from pathlib import Path

# --- GENERAL TOOLING ---
DEFAULT_STEAM_COMPATDATA_PATH = Path(Path.home(), ".steam/steam/steamapps/compatdata/")

def vortex_installer_find():
    current_dir = Path(path.dirname(path.realpath(__file__)))  # Based on the clever code at https://stackoverflow.com/a/5137509
    vortex_installer = list(Path(current_dir).glob("Vortex*.exe"))

    if len(vortex_installer) == 0:
        raise FileNotFoundError(
            "Could not find Vortex mod manager exe!" +
            "\nDue to Nexus Mods limitations, you have to get it yourself. Sorry boss" +
            "\n1. Download it from: https://www.nexusmods.com/site/mods/1?tab=files&file_id=5911" +
            f"\n2. And put it in the same directory as this script: {current_dir}")
    elif len(vortex_installer) > 1:
        print("Found multiple vortex exe's. Please select one!")
        vortex_installer = select(vortex_installer, "Select your preferred vortex installer")
    else:
        vortex_installer = vortex_installer[0]
    return vortex_installer    


def install_vortex_to_prefix(prefix):
    vortex_installer = vortex_installer_find()
    print(vortex_installer)

# --- FALLOUT NEW VEGAS ---

FNV_STEAM_ID = "22380"
def fnv_steam_find():
    default_path = Path(DEFAULT_STEAM_COMPATDATA_PATH, FNV_STEAM_ID, "pfx")

    if not default_path.exists():
        raise NotImplementedError("This script currently expects FNV to be installed in the home folder")

    return default_path


# --- DEFAULT BEHAVIOUR ---


MODES = {
    "fnv-steam": {
        "title": "Fallout: New Vegas (Steam)",
        "find": fnv_steam_find, 
        #"install": 
    }
}


"""meow"""
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



def select_mode():
    def option_title_func(mode):
        return MODES[mode]['title']

    print("Supported games:")
    return select(MODES, "Select a game to manage nexus mod manager for", option_title_func)


if __name__ == "__main__":
    mode = select_mode()

    prefix = mode["find"]()

    actions = [
        "Install Vortex Mod Manager",
    ]

    action = select(actions, "Select action")
    if action == actions[0]:
        install_vortex_to_prefix(prefix)


