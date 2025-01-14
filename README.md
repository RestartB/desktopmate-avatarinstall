# Desktop Mate Avatar Loader Autoinstall
Script / app that automatically installs MelonLoader and the Desktop Mate Avatar Loader mod.

## Contributing
Found a bug? Want to add a feature? Simply make a pull request and I'll take a look. :3

## Usage
> [!CAUTION]
> The autoinstall script only supports Windows 10 and Windows 11. Other versions of Windows and other operating systems (e.g. macOS, Linux) are not supported.

### Prebuilt EXE (easiest)
Use a prebuilt .exe file, built by Github Actions and published in Github Releases. You do not need to install any Python versions for this; simply run the .exe file and follow the steps.

[Download Now](https://github.com/restartb/desktopmate-autoinstall/releases/latest)

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