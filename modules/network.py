# modules/network.py

import subprocess
import time
import emoji
from modules.ssh import test_ssh_connection

def ping_host(ip):
    """Ping a host to check network connectivity."""
    try:
        result = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True)
        if result.returncode == 0:
            print(emoji.emojize("\rTest réussi :white_check_mark:", language='alias'), end="", flush=True)
            return True
        else:
            print("\rTest échoué", end="", flush=True)
            return False
    except Exception as e:
        print(f"\rAn error occurred while pinging: {e}", end="", flush=True)
        return False

def ping_hosts(host_list, key_file=None):
    """Ping multiple hosts and, if reachable, test SSH connectivity."""
    loader = ['◜', '◠', '◝', '◞', '◡', '◟']  # Animation du loader en arc de cercle

    for host in host_list:
        ip = host["ip"]
        username = host["username"]

        # Test de connectivité avec le loader
        print("Test de connectivité", end="", flush=True)
        for i in range(10):  # Durée totale du loader (5 secondes)
            print(f"\rTest de connectivité {loader[i % len(loader)]}", end="", flush=True)
            time.sleep(0.2)

        # Si le ping est réussi, tester la connexion SSH
        if ping_host(ip):
            print("\rTest SSH en cours...", end="", flush=True)
            ssh_success = test_ssh_connection(ip, username, key_file=key_file)
            if ssh_success:
                print(emoji.emojize("\rTest SSH réussi :white_check_mark:", language='alias'), end="", flush=True)
            else:
                print("\rTest SSH échoué", end="", flush=True)
