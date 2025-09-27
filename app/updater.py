import os
import requests
import json
import shutil
import subprocess

# ==============================
# Config
# ==============================
LATEST_URL = "http://your-server.com/latest.json"
CURRENT_VERSION_FILE = "version.txt"
DOWNLOAD_DIR = "downloads"

# ==============================
# Helpers
# ==============================

def get_current_version():
    if not os.path.exists(CURRENT_VERSION_FILE):
        return "0"
    with open(CURRENT_VERSION_FILE, "r") as f:
        return f.read().strip()

def save_current_version(version):
    with open(CURRENT_VERSION_FILE, "w") as f:
        f.write(version)

def fetch_latest_info():
    try:
        response = requests.get(LATEST_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Failed to fetch update info: {e}")
        return None

def download_file(url, dest_path):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        print(f"✅ Downloaded: {dest_path}")
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

# ==============================
# Main Update Flow
# ==============================

def check_for_updates():
    current_version = get_current_version()
    print(f"📦 Current version: {current_version}")

    latest_info = fetch_latest_info()
    if not latest_info:
        return

    latest_version = latest_info.get("version")
    download_url = latest_info.get("download_url")

    if latest_version and download_url:
        print(f"🌍 Latest version: {latest_version}")
        if latest_version > current_version:
            print("⬇️ New version available, downloading...")
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            file_name = os.path.basename(download_url)
            dest_path = os.path.join(DOWNLOAD_DIR, file_name)

            if download_file(download_url, dest_path):
                save_current_version(latest_version)
                print("🚀 Update ready. You can install manually or run the installer.")
                # Example: launch installer (Windows .exe or Linux .AppImage)
                if dest_path.endswith(".exe"):
                    subprocess.Popen([dest_path], shell=True)
                elif dest_path.endswith(".AppImage"):
                    os.chmod(dest_path, 0o755)
                    subprocess.Popen([dest_path])
        else:
            print("✅ Already up-to-date.")
    else:
        print("❌ Invalid latest.json format.")

if __name__ == "__main__":
    check_for_updates()
