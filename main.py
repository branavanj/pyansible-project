# main.py

from modules.network import ping_hosts
from modules.services import install_service, configure_network, configure_service, configure_user
from rich.console import Console

console = Console()

def load_hosts(file_path="config/hosts"):
    """Charge les adresses IP et les noms d'utilisateur depuis le fichier hosts."""
    hosts = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        ip, username = parts[0], parts[1]
                        hosts.append({"ip": ip, "username": username})
                    else:
                        console.print(f"[bold red]Ligne mal formatée dans le fichier hosts :[/bold red] {line}")
        if not hosts:
            console.print("[bold red]Aucune IP trouvée dans le fichier hosts.[/bold red]")
    except FileNotFoundError:
        console.print(f"[bold red]Le fichier {file_path} est introuvable.[/bold red]")
    return hosts

def main():
    # Charger les adresses IP et utilisateurs depuis le fichier hosts
    host_list = load_hosts()
    if not host_list:
        console.print("[bold red]Aucune adresse IP n'a été chargée. Vérifiez le fichier hosts.[/bold red]")
        return

    # Tester automatiquement la connectivité réseau et SSH avant d'afficher le menu
    if not ping_hosts(host_list):
        console.print("[bold red]La connectivité réseau ou SSH a échoué pour au moins un hôte.[/bold red]")
        return

    # Afficher le menu principal
    console.print("[bold cyan]Bienvenue dans le menu de gestion de votre projet d'administration[/bold cyan]")
    while True:
        console.print("\nChoisissez une option :")
        console.print("1. Installer un service")
        console.print("2. Configurer la carte réseau")
        console.print("3. Configurer un service")
        console.print("4. Configurer les utilisateurs")
        console.print("0. Quitter")

        choice = input("Entrez votre choix : ")

        if choice == "1":
            console.print("\nChoisissez un service à installer :")
            console.print("1. Serveur Web")
            console.print("2. Serveur LDAP")
            console.print("3. Serveur FTP")
            console.print("4. Serveur DNS")
            service_choice = input("Entrez votre choix de service : ")
            for host in host_list:
                install_service(service_choice, host)

        elif choice == "2":
            for host in host_list:
                configure_network(host)

        elif choice == "3":
            for host in host_list:
                configure_service(host)

        elif choice == "4":
            for host in host_list:
                configure_user(host)

        elif choice == "0":
            console.print("[bold yellow]Fermeture du menu...[/bold yellow]")
            break

        else:
            console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")

if __name__ == "__main__":
    main()
