import os
import subprocess
import time
import requests
import json

#use this to if files are not accesible
#sudo chmod -R 777 ./world/

def start_ngrok(port):
    # Start ngrok in a new subprocess
    ngrok = subprocess.Popen(["ngrok", "tcp", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Allow ngrok to initialize

    # Get the ngrok URL from the API
    url = "http://127.0.0.1:4040/api/tunnels"
    response = requests.get(url)
    data = json.loads(response.text)
    tunnel_url = data['tunnels'][0]['public_url']
    return tunnel_url

def isFirstRun():
    if os.path.isdir("./versions") & os.path.isdir("./libraries"):
        return False
    else:
        return True
    

minecraft_port = 25565

#main
if isFirstRun():
    subprocess.run(["bash", "minecraft.sh"])

else:
    ngrok_url = start_ngrok(minecraft_port)
    print(f"ngrok tunnel started: {ngrok_url}")
    subprocess.run(["java", "-Xms16G", "-Xmx16G", "-jar", "server.jar", "nogui"])