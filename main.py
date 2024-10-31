# main.py

from modules.network import ping_hosts

def load_hosts(file_path="config/hosts"):
    """Charge les adresses IP et les noms d'utilisateur depuis le fichier hosts."""
    hosts = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                # Ignore les lignes vides et les commentaires
                if line.strip() and not line.startswith("#"):
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        ip, username = parts[0], parts[1]
                        hosts.append({"ip": ip, "username": username})
                    else:
                        print(f"Ligne mal formatée dans le fichier hosts : {line}")
        if not hosts:
            print("Aucune IP trouvée dans le fichier hosts.")
    except FileNotFoundError:
        print(f"Le fichier {file_path} est introuvable.")
    return hosts

def main():
    # Charger les adresses IP et utilisateurs depuis le fichier hosts
    host_list = load_hosts()
    if not host_list:
        print("Aucune adresse IP n'a été chargée. Vérifiez le fichier hosts.")
        return

    # Début des tests de connectivité réseau et SSH
    print("Début des tests de connectivité réseau et SSH...")
    reachable_hosts = ping_hosts(host_list)


if __name__ == "__main__":
    main()
