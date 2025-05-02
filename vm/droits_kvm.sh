#!/bin/bash

# Vérifiez si le script est exécuté en tant que root
if [ "$EUID" -ne 0 ]; then
  echo "Veuillez exécuter ce script en tant que root ou avec sudo."
  exit 1
fi

# Demandez le nom de l'utilisateur
read -p "Entrez le nom de l'utilisateur à ajouter au groupe kvm: " USERNAME

# Ajoutez l'utilisateur au groupe kvm
usermod -aG kvm $USERNAME
echo "L'utilisateur $USERNAME a été ajouté au groupe kvm."

# Ajustez les permissions des répertoires
chown -R :kvm /etc/libvirt/qemu/
chmod -R 775 /etc/libvirt/qemu/
echo "Permissions ajustées pour /etc/libvirt/qemu/."

chown -R :kvm /var/lib/libvirt/images/
chmod -R 775 /var/lib/libvirt/images/
echo "Permissions ajustées pour /var/lib/libvirt/images/."

# Demandez à l'utilisateur de se reconnecter
echo "Veuillez vous déconnecter et vous reconnecter pour que les changements prennent effet."
