# main.py

from modules.network import ping_hosts
# from modules.services import install_service, configure_network, configure_service, configure_user
from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer

console = Console()

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
                        console.print(f"[bold red]Ligne mal formatée dans le fichier hosts :[/bold red] {line}")
        if not hosts:
            console.print("[bold red]Aucune IP trouvée dans le fichier hosts.[/bold red]")
    except FileNotFoundError:
        console.print(f"[bold red]Le fichier {file_path} est introuvable.[/bold red]")
    return hosts

def main_menu():
    console.print(Panel("[bold cyan]Bienvenue dans le menu de gestion de votre projet d'administration[/bold cyan]"))
    
    while True:
        choice = inquirer.select(
            message="Choisissez une option :",
            choices=[
                "Tester la connectivité réseau et SSH",
                "Installer un service",
                "Configurer la carte réseau",
                "Configurer un service",
                "Configurer les utilisateurs",
                "Quitter"
            ],
            default="Quitter"
        ).execute()

        if choice == "Tester la connectivité réseau et SSH":
            # Tester la connectivité
            host_list = load_hosts()
            if not host_list:
                console.print("[bold red]Aucune adresse IP n'a été chargée. Vérifiez le fichier hosts.[/bold red]")
            else:
                ping_hosts(host_list)

        elif choice == "Installer un service":
            # Sous-menu pour installer un service
            service_choice = inquirer.select(
                message="Choisissez un service à installer :",
                choices=[
                    "Serveur Web",
                    "Serveur LDAP",
                    "Serveur FTP",
                    "Serveur DNS",
                    "Retour"
                ],
                default="Retour"
            ).execute()
            
            if service_choice != "Retour":
                print("ll")

        elif choice == "Configurer la carte réseau":
            print("ll")

        elif choice == "Configurer un service":
            print("ll")

        elif choice == "Configurer les utilisateurs":
            print("ll")

        elif choice == "Quitter":
            console.print("[bold yellow]Fermeture du menu...[/bold yellow]")
            break

if __name__ == "__main__":
    main_menu()
