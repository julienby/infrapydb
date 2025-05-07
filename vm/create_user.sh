#!/bin/bash

# Vérifier si le nom d'utilisateur et le mot de passe ont été fournis en arguments
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <nom_utilisateur> <mot_de_passe>"
  exit 1
fi

# Nom de l'utilisateur et mot de passe fournis en arguments
USERNAME=$1
DEFAULT_PASSWORD=$2

# Créer l'utilisateur avec un shell bash
sudo useradd -m -s /bin/bash $USERNAME

# Définir le mot de passe par défaut pour l'utilisateur
echo "$USERNAME:$DEFAULT_PASSWORD" | sudo chpasswd

# Ajouter l'utilisateur au groupe sudo
sudo usermod -aG sudo $USERNAME

# Vérifier que l'utilisateur a été créé et a les bons privilèges
id $USERNAME
groups $USERNAME

echo "L'utilisateur $USERNAME a été créé avec succès avec le mot de passe fourni et des privilèges sudo."
