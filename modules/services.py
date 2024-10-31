# modules/services.py

import paramiko
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn

console = Console()

def execute_remote_command(host, command):
    """Exécute une commande sur une machine distante via SSH."""
    ip = host["ip"]
    username = host["username"]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, username=username)
        stdin, stdout, stderr = client.exec_command(command)
        stdout.channel.recv_exit_status()  # Attend la fin de la commande
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            console.print(f"[bold red]Erreur sur {ip} : {error}[/bold red]")
        else:
            console.print(f"[bold green]Commande réussie sur {ip} : {output}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Erreur de connexion SSH sur {ip} : {e}[/bold red]")
    finally:
        client.close()

def install_service(service_name, host):
    """Installe un service sur une machine distante via SSH."""
    service_packages = {
        "1": "httpd",  # Serveur Web
        "2": "openldap-servers openldap-clients",  # Serveur LDAP
        "3": "vsftpd",  # Serveur FTP
        "4": "bind bind-utils"  # Serveur DNS
    }

    if service_name not in service_packages:
        console.print(f"[bold red]Service inconnu : {service_name}[/bold red]")
        return

    package = service_packages[service_name]
    command = f"sudo dnf install -y {package}"

    console.print(f"[bold green]Installation de {package} sur {host['ip']}...[/bold green]")

    # Barre de progression Rich
    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=None, complete_style="green"),
        TextColumn("[bold blue]{task.percentage:>3.1f}%"),
        TextColumn("• [bold yellow]{task.completed}/{task.total} étapes"),
        console=console,
    ) as progress:
        task = progress.add_task("Installation", total=1)

        # Exécute la commande d'installation à distance
        execute_remote_command(host, command)
        progress.update(task, advance=1)

    console.print(f"[bold green]{package} installé avec succès sur {host['ip']} ![/bold green]")

def configure_network(host):
    """Configure la carte réseau sur une machine distante via SSH."""
    command = "sudo nmcli con mod eth0 ipv4.addresses 192.168.1.100/24 && sudo nmcli con up eth0"
    execute_remote_command(host, command)

def configure_service(host):
    """Configure un service sur une machine distante via SSH."""
    console.print("[bold yellow]Configuration du service sur la machine distante...[/bold yellow]")
    # Ajouter des commandes spécifiques pour configurer un service
    execute_remote_command(host, "echo 'Configuration du service...'")

def configure_user(host):
    """Ajoute ou configure un utilisateur sur une machine distante via SSH."""
    console.print("[bold yellow]Configuration des utilisateurs sur la machine distante...[/bold yellow]")
    username = input("Entrez le nom de l'utilisateur : ")
    command = f"sudo adduser {username} && sudo passwd {username}"
    execute_remote_command(host, command)
