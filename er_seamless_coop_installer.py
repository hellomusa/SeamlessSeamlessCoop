import requests
import os
import zipfile
import shutil
import json

CONFIG_FILE = 'config.json'
GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/releases/latest"
GITHUB_DOWNLOAD_URL = "https://github.com/{owner}/{repo}/releases/download/{version}/ersc.zip"
OWNER = "LukeYui"
REPO = "EldenRingSeamlessCoopRelease"

def load_or_create_config():
    """
    Load existing config or create a new one by prompting the user.
    Returns a dictionary with 'elden_ring_path' and 'coop_password'.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)

    config = {}
    config['elden_ring_path'] = get_valid_path("Enter your Elden Ring installation directory: ")
    config['coop_password'] = input("Enter your desired co-op session password: ")

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

    return config

def get_valid_path(prompt):
    """Repeatedly prompt the user for a valid directory path."""
    while True:
        path = input(prompt)
        if os.path.exists(path):
            return path
        print("The specified path does not exist. Please try again.")

def update_ersc_settings_file(extract_folder, password):
    """Update the co-op password in the mod's INI file."""
    ini_path = os.path.join(extract_folder, 'SeamlessCoop', 'ersc_settings.ini')
    if not os.path.exists(ini_path):
        print(f"WARNING: {ini_path} not found")
        return

    with open(ini_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('cooppassword'):
            lines[i] = f'cooppassword = {password}\n'
            with open(ini_path, 'w') as file:
                file.writelines(lines)
            print(f"Updated co-op password in {ini_path}")
            return

    print("WARNING: 'cooppassword' line not found in ersc_settings.ini")

def download_latest_release():
    """
    Download the latest release of the mod and extracts the .zip. 
    Returns a tuple of (filename, extract_folder).
    """
    response = requests.get(GITHUB_API_URL.format(owner=OWNER, repo=REPO))
    latest_version = response.json()['tag_name']
    download_url = GITHUB_DOWNLOAD_URL.format(owner=OWNER, repo=REPO, version=latest_version)

    filename = f"ersc_{latest_version}.zip"
    response = requests.get(download_url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to download the file. Status code: {response.status_code}")

    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Successfully downloaded {filename}")

    extract_folder = f"ersc_{latest_version}"
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    print(f"Successfully extracted contents to {extract_folder}")

    return filename, extract_folder

def install_mod(extract_folder, elden_ring_path):
    """Install the mod to the Elden Ring directory."""
    for item in os.listdir(extract_folder):
        src = os.path.join(extract_folder, item)
        dst = os.path.join(elden_ring_path, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
    print(f"Successfully installed mod to {elden_ring_path}")

def cleanup(filename, extract_folder):
    """Remove temporary files and folders."""
    shutil.rmtree(extract_folder)
    os.remove(filename)
    print("Cleaned up temporary files")

def main():
    """Main function to orchestrate the mod download and installation process."""
    config = load_or_create_config()
    try:
        filename, extract_folder = download_latest_release()
        update_ersc_settings_file(extract_folder, config['coop_password'])
        install_mod(extract_folder, config['elden_ring_path'])
        cleanup(filename, extract_folder)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()