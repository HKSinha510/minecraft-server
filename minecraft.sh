#!/bin/bash
## ngrok tcp 25565
# Clear the screen
clear

source ./.env

# LEAVE CREDITS
# Ask the user for the Minecraft server script URL
#https://mcversions.net/download/1.21.1
read -p "Please enter the URL of the Minecraft server script (press Enter to use the default URL(1.21.1)): " server_url
server_url=${server_url:-"https://piston-data.mojang.com/v1/objects/59353fb40c36d304f2035d51e7d6e6baa98dc05c/server.jar"}

# Download the Minecraft server script
wget -O server.jar $server_url

# Download openjdk-21-jdk
sudo apt-get update
sudo apt-get install openjdk-21-jdk -y

# Ask the user if they accept the Minecraft EULA
#read -p "Do you accept the Minecraft EULA? (Type 'yes' or 'y' to accept): " eula_acceptance

#ngrok setup & install
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xf ngrok-v3-stable-linux-amd64.tgz
./ngrok config add-authtoken $NGROK_TOKEN


if true; then
    # Ask the user for the amount of RAM to allocate
    read -p "How much RAM would you like to allocate to the Minecraft server (in GB)? " ram_amount

    # Modify the Java command with the user's response
    java_command="java -Xms${ram_amount}G -Xmx${ram_amount}G -jar server.jar nogui"

    # Launch the Minecraft server
    $java_command

    # Modify the eula.txt file to set 'true'
    echo "eula=true" > eula.txt

    # Restart the Minecraft server with the new configurations
    $java_command
else
    echo "You must accept the Minecraft EULA to proceed. Aborting."
fi
