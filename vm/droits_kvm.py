#!/usr/bin/env python3

import os
import pwd
import grp
import subprocess
import sys

def check_root():
    """Vérifie si le script est exécuté en tant que root"""
    if os.geteuid() != 0:
        print("Veuillez exécuter ce script en tant que root ou avec sudo.")
        sys.exit(1)

def add_user_to_kvm_group(username):
    """Ajoute l'utilisateur au groupe kvm"""
    try:
        subprocess.run(['usermod', '-aG', 'kvm', username], check=True)
        print(f"L'utilisateur {username} a été ajouté au groupe kvm.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'ajout de l'utilisateur au groupe kvm: {e}")
        sys.exit(1)

def adjust_permissions():
    """Ajuste les permissions des répertoires"""
    directories = [
        '/etc/libvirt/qemu/',
        '/var/lib/libvirt/images/'
    ]
    
    for directory in directories:
        try:
            # Récupérer le GID du groupe kvm
            kvm_gid = grp.getgrnam('kvm').gr_gid
            
            # Changer le groupe propriétaire
            os.chown(directory, -1, kvm_gid)
            for root, dirs, files in os.walk(directory):
                os.chown(root, -1, kvm_gid)
                for file in files:
                    os.chown(os.path.join(root, file), -1, kvm_gid)
            
            # Définir les permissions 775
            os.chmod(directory, 0o775)
            for root, dirs, files in os.walk(directory):
                os.chmod(root, 0o775)
                for file in files:
                    os.chmod(os.path.join(root, file), 0o775)
                    
            print(f"Permissions ajustées pour {directory}.")
        except Exception as e:
            print(f"Erreur lors de l'ajustement des permissions pour {directory}: {e}")
            sys.exit(1)

def main():
    check_root()
    
    # Demander le nom de l'utilisateur
    username = input("Entrez le nom de l'utilisateur à ajouter au groupe kvm: ")
    
    # Vérifier si l'utilisateur existe
    try:
        pwd.getpwnam(username)
    except KeyError:
        print(f"L'utilisateur {username} n'existe pas.")
        sys.exit(1)
    
    add_user_to_kvm_group(username)
    adjust_permissions()
    
    print("Veuillez vous déconnecter et vous reconnecter pour que les changements prennent effet.")

if __name__ == "__main__":
    main() 