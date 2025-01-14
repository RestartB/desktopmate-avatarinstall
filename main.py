import os
import winreg
import zipfile

import requests
import vdf
from colorama import Fore, Style
from tqdm import tqdm

print(f"{Style.BRIGHT}Desktop Mate Mod Installer v1.0")
print("2025, RestartB\n")

print(f"Please ensure that Desktop Mate has been opened once before running the script, and that it is not currently running.{Style.RESET_ALL}")
input("Press enter to continue...")

# Get installer
print("Detecting operating system...")
if os.name != "nt":
    print(f"{Fore.RED}Operating system: {Style.BRIGHT}{os.name}{Style.RESET_ALL}")
    print(f"{Fore.RED}Error: This script is only compatible with Windows.{Style.RESET_ALL}")
    exit(1)
else:
    print(f"{Fore.GREEN}Operating system: {Style.BRIGHT}Windows{Style.RESET_ALL}\n")

# Find Steam
print("Detecting Steam...")

try:
    # Connect to registry and open Steam key
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
        with winreg.OpenKey(hkey, r"Software\Valve\Steam") as steam_key:
            # Get Steam path
            steam_path = os.path.normpath(winreg.QueryValueEx(steam_key, "SteamPath")[0])
            print(f"{Fore.GREEN}Steam installation found at: {Style.BRIGHT}{steam_path}{Style.RESET_ALL}\n")
            
            # Close registry keys
            winreg.CloseKey(steam_key)
except Exception as e:
    print(f"{Fore.RED}Error: Could not detect Steam installation.{Style.RESET_ALL}")
    print(f"Error details: {e}")

    exit(1)

# Open Steam library
print("Opening Steam Library...")
library = vdf.load(open(os.path.join(steam_path, "steamapps", "libraryfolders.vdf"), "r"))

# Find Desktop Mate install
print("Finding Desktop Mate install...")
mate_path = None

for library_folder in library["libraryfolders"]:
    library_folder = library["libraryfolders"][library_folder]
    
    # Check if Desktop Mate is in the current library
    if "3301060" in library_folder["apps"]:
        if os.path.exists(os.path.join(library_folder['path'], "steamapps", "common", "Desktop Mate")):
            mate_path = os.path.join(library_folder['path'], "steamapps", "common", "Desktop Mate")
            print(f"{Fore.GREEN}Found Desktop Mate: {Style.BRIGHT}{mate_path}{Style.RESET_ALL}\n")
            break

if mate_path is None:
    print(f"{Fore.RED}Error: Could not find Desktop Mate installation.{Style.RESET_ALL}")
    exit(1)

# Download .NET 6
print("Downloading .NET 6...")
os.system("winget install Microsoft.DotNet.Runtime.6 --accept-package-agreements --accept-source-agreements")

# Download MelonLoader
print("\nDownloading MelonLoader...")

response = requests.get("https://github.com/LavaGang/MelonLoader/releases/latest/download/MelonLoader.x64.zip")
file_size = int(response.headers.get('content-length', 0))

# Make temp directory if it doesn't exist
if not os.path.exists("mate-install-temp"):
    os.mkdir("mate-install-temp")

# Save loader to file, show loading bar
with open(os.path.join("mate-install-temp", "melonloader.zip"), "wb") as handle:
    for data in tqdm(response.iter_content(), total=file_size, unit='iB', unit_scale=True):
        handle.write(data)

print(f"{Fore.GREEN}Downloaded!{Style.RESET_ALL}\n")

# Download mod
print("Downloading DesktopMate Mod...")

response = requests.get("https://github.com/YusufOzmen01/desktopmate-custom-avatar-loader/releases/latest/download/CustomAvatarLoader.zip")
file_size = int(response.headers.get('content-length', 0))

# Save mod to file, show loading bar
with open(os.path.join("mate-install-temp", "mod.zip"), "wb") as handle:
    for data in tqdm(response.iter_content(), total=file_size, unit='iB', unit_scale=True):
        handle.write(data)

print(f"{Fore.GREEN}Downloaded!{Style.RESET_ALL}\n")

print("Extracting files...")
try:
    # Extract MelonLoader
    with zipfile.ZipFile(os.path.join("mate-install-temp", "melonloader.zip")) as zf:
        zf.extractall(mate_path)

    # Extract Mod
    with zipfile.ZipFile(os.path.join("mate-install-temp", "mod.zip")) as zf:
        zf.extractall(mate_path)

    print(f"{Fore.GREEN}Files extracted!{Style.RESET_ALL}\n")
except zipfile.BadZipFile:
    print(f"{Fore.RED}Error: One or more zip files are corrupted{Style.RESET_ALL}")
    exit(1)
except Exception as e:
    print(f"{Fore.RED}Error extracting files: {e}{Style.RESET_ALL}")
    exit(1)

# Clean up
print("Cleaning up...")
os.remove(os.path.join("mate-install-temp", "melonloader.zip"))
os.remove(os.path.join("mate-install-temp", "mod.zip"))
os.rmdir("mate-install-temp")
print(f"{Fore.GREEN}Cleaned up!{Style.RESET_ALL}\n")

# Done
print(f"{Fore.GREEN}All done!{Style.RESET_ALL}")
print("Press enter to run Desktop Mate (press open when prompted), or press CTRL+C / close the window to exit.\n")

print(f"{Style.BRIGHT}** Note **{Style.RESET_ALL}")
print("The first launch of Desktop Mate may take longer than usual, this is normal as the mod loader is injecting itself into Desktop Mate.")

# Run Desktop Mate if user presses enter
input("")
os.system("start steam://rungameid/3301060")