#!/usr/bin/env python3

import sys
import subprocess
import getpass

def create_user(username, password):
    try:
        # Create user with bash shell
        subprocess.run(['sudo', 'useradd', '-m', '-s', '/bin/bash', username], check=True)
        
        # Set password using chpasswd
        subprocess.run(['echo', f'{username}:{password}', '|', 'sudo', 'chpasswd'], shell=True, check=True)
        
        # Add user to sudo group
        subprocess.run(['sudo', 'usermod', '-aG', 'sudo', username], check=True)
        
        # Verify user creation and privileges
        subprocess.run(['id', username], check=True)
        subprocess.run(['groups', username], check=True)
        
        print(f"User {username} has been successfully created with the provided password and sudo privileges.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    # Check if username and password are provided as arguments
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <username> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    create_user(username, password)

if __name__ == "__main__":
    main() 