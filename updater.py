import os
import shutil
import sys

import requests
from PySide6.QtWidgets import QApplication, QMessageBox

# todo: change to organization name and the actual app name
OWNER = 'RuthvikSaiKumar'
REPO = 'test'
ASSET_NAME = 'app.txt'  # Name of the asset to download

# Path to the main application executable
APP_PATH = 'app.txt'
VERSION_FILE_PATH = 'version.txt'


# Function to get the latest release from GitHub
def get_latest_release():
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/releases/latest'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print("Failed to fetch latest release.")
    return None


# Function to download the asset
def download_asset(asset_url, download_path):
    response = requests.get(asset_url, stream=True)
    if response.status_code == 200:
        with open(download_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"Downloaded {ASSET_NAME} to {download_path}.")
        return True
    else:
        print(f"Failed to download {ASSET_NAME}.")
        return False


# Function to read the current version from the version file
def read_current_version():
    if os.path.exists(VERSION_FILE_PATH):
        try:
            with open(VERSION_FILE_PATH, 'r') as file:
                return file.readlines()[1].strip()
        except:
            print("Failed to read the current version.")
            return None
    return None


# Function to write the new version to the version file
def write_new_version(new_version):
    with open(VERSION_FILE_PATH, 'w') as file:
        # write a comment for the user to not edit the file
        file.write("# Do NOT edit this file. It is automatically generated by the application.\n")
        file.write(new_version)


def main():
    app = QApplication(sys.argv)

    current_version = read_current_version()
    latest_release = get_latest_release()
    if not latest_release:
        return

    latest_version = latest_release['tag_name']
    asset_url = next(
        (asset['browser_download_url'] for asset in latest_release['assets'] if asset['name'] == ASSET_NAME),
        None)

    if not asset_url:
        print(f"Asset {ASSET_NAME} not found in the latest release.")
        return

    # Check if the latest version is different from the current version
    if current_version == latest_version:
        print(f"Current version ({current_version}) is up-to-date.")
        return

    # Ask the user if they want to update
    msg_box = QMessageBox()
    msg_box.setText(f"A new version ({latest_version}) of the application is available. Do you want to update?")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    reply = msg_box.exec()

    if reply == QMessageBox.StandardButton.Yes:
        # Download the new version
        download_path = os.path.join(os.path.dirname(APP_PATH), ASSET_NAME)
        if download_asset(asset_url, download_path):
            # Replace the old version with the new one
            os.replace(download_path, APP_PATH)
            write_new_version(latest_version)
            print("Application updated successfully.")
        else:
            print("Failed to update the application.")
    else:
        print("Update canceled by the user.")

    sys.exit(0)


if __name__ == '__main__':
    main()
