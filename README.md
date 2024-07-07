# Elden Ring Seamless Co-op Mod Installer

This Python script automates the process of downloading and installing the Seamless Co-op mod for Elden Ring. It fetches the latest version of the mod from GitHub, installs it to your Elden Ring directory, and configures the co-op password.

## Features

- Automatically downloads the latest version of the Seamless Co-op mod
- Installs the mod to your Elden Ring game directory
- Configures the co-op password in the mod's settings file
- Saves your Elden Ring installation path and co-op password for future use

## Requirements

- Python 3.6 or higher
- `requests` library (for downloading the mod)

## Installation

1. Ensure you have Python installed on your system.
2. Install the required `requests` library:
   ```
   pip install requests
   ```
3. Download the `er_seamless_coop_installer.py` script to your local machine.

## Usage

1. Run the script:
   ```
   python er_seamless_coop_installer.py
   ```
2. On first run, you'll be prompted to enter:
   - Your Elden Ring installation directory
   - Your co-op session password
3. The script will download the latest mod version, install it, and configure the password.

## Configuration

The script creates a `config.json` file to store your Elden Ring installation path and co-op password. You can manually edit this file if needed.

## Troubleshooting

- If the script fails to download the mod, check your internet connection and ensure the GitHub repository is accessible.
- If installation fails, verify that the Elden Ring installation path is correct and that you have write permissions to that directory.

## Disclaimer

This script is not officially associated with Elden Ring or the Seamless Co-op mod. Use at your own risk. Always backup your game files before modding.
