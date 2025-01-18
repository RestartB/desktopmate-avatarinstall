# Desktop Mate Avatar Loader Autoinstall
Script that automatically installs [MelonLoader](https://github.com/LavaGang/MelonLoader) and the [Desktop Mate Avatar Loader mod](https://github.com/YusufOzmen01/desktopmate-custom-avatar-loader).

## Contributing
Found a bug? Make an issue and I'll take a look. Want to add a feature or submit a bug fix? Simply make a pull request! :3

## Usage
> [!CAUTION]
> The autoinstall script only supports Windows 10 and Windows 11. Other versions of Windows and other operating systems (e.g. macOS, Linux) are not supported.

### Powershell / Python EXE (easiest)
I provide a Powershell script and a Python based prebuilt EXE file. The Powershell script can be run with one command from the command line, the Python version requires you to download the .exe file.
#### Powershell
To run the script, use the following command:
`powershell -ExecutionPolicy ByPass -c "irm https://github.com/RestartB/desktopmate-avatarinstall/releases/latest/setup.ps1 | iex"`
#### Python
Use the following link to download the Python version of the installer. Once it's downloaded, you can run it like a normal exe file.\
[Download Now](https://github.com/restartb/desktopmate-avatarinstall/releases/latest)

### Manual
You can optionally choose to run the Python script yourself for more transparency. Follow the instructions below to run this.
#### uv Package Manager
I prefer to use the `uv` package manager for this. It manages Python versions, installing the packages and running the script for you. Follow the steps below to use it:
1. Clone the git repo
2. Install `uv` if you don't already have it - `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
3. Open a terminal in the directory of the cloned repo
4. Run the script - `uv run main.py`. uv will automatically set up a venv and download dependencies
#### Other Package Managers
I have built the project on Python `3.13`. Most other recent versions of Python 3 should also work. I have provided a `pyproject.toml` file. There are many Python package managers that support this, e.g. `pip`, `poetry`. Most should work fine.
