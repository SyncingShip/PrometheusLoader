import os, re, json, subprocess

def find_installation():
    name = "Hades.exe"
    drives = get_drives()
    results = []
    for path in drives:
        print("Searching drive " + path)
        for root, dirs, files in os.walk(path):
            if name in files:
                path = os.path.dirname(root)
                print("Found hades installation at " + path)
                return(path)

def apply_patches(patch_list, game_directory):
    for patch in patch_list:
        print("Applying " + patch)
        subprocess.run(["git", "apply", patch], cwd=game_directory+"\Content\Scripts")

def find_patches():
    patch_files = []
    for directory, subdirectories, files in os.walk(".\Mods"):
        for file in files:
            if re.search(r".+?\.patch", file):
                patch_files.append(os.path.abspath(os.path.join(directory, file)))
    return patch_files

def get_drives():
    return re.findall(r"[A-Z]+:.*$", os.popen("mountvol /").read(), re.MULTILINE)

def main():
    with open('config.json') as f:
        config = json.load(f)

    if config["hades_install"] == "unassigned":
        response = input("Hades installation not assigned\n" +
              "0. Exit\n" + 
              "1. Auto detect Hades installation (Recommended)\n" + 
              "2. Manually locate Hades installation\n > ")
        while not(re.search(r"^[0-2]$", response)):
            response = input("Please enter 1 or 2 > ")

        if response == "0":
            exit()
        elif response == "1":
            location = find_installation()
            config["hades_install"] = location
            game_dir = location

            with open('config.json', 'w') as outfile:
                json.dump(config, outfile)
        elif response == "2":
            print("Please edit config.json with the path to your Hades installation.\n For example \"hades_install\" : \"C:\\\\Games\\\\Hades\". Double backslashes are needed")
    
    else:
        game_dir = config["hades_install"]

    input("Ready to patch game. Press enter to continue")
    apply_patches(find_patches(), game_dir)
    input("Patching completed. To uninstall mods, verify through the Epic Games Store. \nPress enter to finish")

main()