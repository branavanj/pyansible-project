# modules/ssh.py

import paramiko
import emoji

def test_ssh_connection(ip, username, key_file=None):
    """Test SSH connection to a host using key-based authentication."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connexion SSH en utilisant une clé privée si `key_file` est spécifié, sinon authentification par défaut
        if key_file:
            client.connect(ip, username=username, key_filename=key_file)
        else:
            client.connect(ip, username=username)

        return True
    except Exception as e:
        # Affiche le message d'erreur si la connexion échoue
        print(f"\rSSH connection to {ip} failed: {e}", flush=True)
        return False
    finally:
        client.close()
