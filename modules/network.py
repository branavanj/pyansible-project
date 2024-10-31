# modules/network.py

import subprocess
import paramiko
from rich.console import Console

console = Console()

def ping_host(ip):
    """Ping une machine pour vérifier la connectivité réseau."""
    try:
        result = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def test_ssh_connectivity(host):
    """Teste la connectivité SSH en utilisant Paramiko."""
    ip = host["ip"]
    username = host["username"]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, username=username)
        console.print(f"[bold green]Connexion SSH réussie pour {ip}[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Échec de la connexion SSH pour {ip} : {e}[/bold red]")
        return False
    finally:
        client.close()

def ping_hosts(host_list):
    """Teste la connectivité réseau et SSH pour plusieurs machines."""
    all_successful = True
    for host in host_list:
        ip = host["ip"]
        if not ping_host(ip):
            console.print(f"[bold red]Connectivité réseau échouée pour {ip}[/bold red]")
            all_successful = False
        elif not test_ssh_connectivity(host):
            all_successful = False

    if all_successful:
        console.print("[bold green]Connectivité réseau et SSH réussie pour toutes les machines ![/bold green]")
    return all_successful
