#!/usr/bin/env python3
"""
Setup script for the Weather Dashboard application.
This script helps users set up their environment variables.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with user input"""
    env_path = Path('.env')
    
    # Don't overwrite existing .env file
    if env_path.exists():
        print(".env file already exists. Please edit it manually or delete it to run setup again.")
        return
    
    print("Setting up your Weather Dashboard environment...")
    print("Please provide the following information:")
    
    email = input("Your email address (for NWS API identification): ").strip()
    
    # Create .env file
    with open(env_path, 'w') as f:
        f.write(f"APP_EMAIL={email}\n")
    
    print("\nEnvironment file created successfully!")
    print("You can edit these values anytime by modifying the .env file")

if __name__ == "__main__":
    create_env_file() 