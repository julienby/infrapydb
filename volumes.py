import socket
import subprocess
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
HEADERS = {
    "accept": "application/json",
    "xc-token": API_TOKEN,
    "Content-Type": "application/json"
}

def get_hostname():
    return socket.gethostname()

def get_volumes_to_monitor(hostname):
    params = {
        "fields": "Id,Path",
        "where": f"where=(HYPERVISEURS,like,{hostname}%)",
        "limit": 100
    }
    response = requests.get(API_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json().get("list", [])

def get_disk_usage(path):
    try:
        output = subprocess.check_output(["df", "-B1G", "--output=size,used", path], text=True)
        lines = output.strip().split("\n")
        if len(lines) < 2:
            raise ValueError("Invalid df output")
        size_str, used_str = lines[1].split()
        size_gb = int(size_str)
        used_gb = int(used_str)
        return size_gb, used_gb
    except Exception as e:
        print(f"Erreur lors de l'analyse du volume {path} : {e}")
        return None, None

def update_volume_usage(volume_id, size, used):
    payload = {
        "id": str(volume_id),
        "Size": size,
        "Used": used
    }
    response = requests.patch(API_URL, headers=HEADERS, data=json.dumps(payload))
    if response.ok:
        print(f"✅ Volume ID {volume_id} mis à jour avec succès.")
    else:
        print(f"❌ Erreur mise à jour volume ID {volume_id} : {response.status_code} — {response.text}")

def main():
    hostname = get_hostname()
    print(f"🔍 Hyperviseur : {hostname}")
    volumes = get_volumes_to_monitor(hostname)

    for volume in volumes:
        volume_id = volume.get("Id")
        path = volume.get("Path")
        if not path:
            continue

        size, used = get_disk_usage(path)
        if size is not None and used is not None:
            print(f"📦 Volume {path} (ID {volume_id}) — Taille : {size} Go, Utilisé : {used} Go")
            update_volume_usage(volume_id, size, used)

if __name__ == "__main__":
    main()
