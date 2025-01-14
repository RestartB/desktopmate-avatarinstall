import os
import winreg
import vdf
from colorama import Style, Fore
from tqdm import tqdm
import requests

print("DesktopMate Mod Installer")
print("2025, RestartB\n")

# Get installer
print("Detecting operating system...")
if os.name != "nt":
    print(f"{Fore.RED}Operating system: {Style.BRIGHT}{os.name}{Style.RESET_ALL}")
    print(f"{Fore.RED}Error: This script is only compatible with Windows.{Style.RESET_ALL}")
    exit(1)
else:
    print(f"{Fore.GREEN}Operating system: {Style.BRIGHT}Windows\n{Style.RESET_ALL}")

# Find Steam
print("Detecting Steam...")

try:
    # Connect to registry and open Steam key
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
        with winreg.OpenKey(hkey, r"Software\Valve\Steam") as steam_key:
            # Get Steam path
            steam_path = os.path.normpath(winreg.QueryValueEx(steam_key, "SteamPath")[0])
            print(f"{Fore.GREEN}Steam installation found at: {Style.BRIGHT}{steam_path}\n{Style.RESET_ALL}")
            
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
        mate_path = os.path.join(library_folder['path'], "common", "Desktop Mate")
        
        if os.path.exists(mate_path):
            print(f"{Fore.GREEN}Found DesktopMate: {Style.BRIGHT}{mate_path}\n{Style.RESET_ALL}")
            break
        else:
            mate_path = None

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