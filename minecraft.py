import os
import subprocess
import time
import json
import threading
import urllib.request

#use this to if files are not accesible
#sudo chmod -R 777 ./world/

minecraft_port = 25565
ram_amount = 16
tcp_link = None
server_process = None

local_world_path = './world/'       #path
upload_interval = 700               #interval

def send_command(command):
    if server_process:
        server_process.stdin.write(command + "\n")
        server_process.stdin.flush()

def read_env(environment_variable) -> str:
    with open("./.env") as f:
        lines = {j.split("=")[0]: j.split("=")[1] for j in [i.strip() for i in f.readlines()]}
        return lines[environment_variable]
    
def isFirstRun():
    if os.path.isdir("./versions") & os.path.isdir("./libraries"):
        return False
    else:
        return True
    
def manual_input():
    while True:
        command = input()  # Wait for user input
        if command == 'tcp':
            print(tcp_link)
        else:
            send_command(command)

def start_server():
    global server_process
    server_process = subprocess.Popen(
        ["java", "-Xms16G", "-Xmx16G", "-jar", "server.jar", "nogui"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    while True:
        output = server_process.stdout.readline()
        if output:
            print(output.strip())  # Display server output
        else:
            break

def start_ngrok():
    import requests
    
    # Start ngrok in a new subprocess
    subprocess.run(["./ngrok", "config", "add-authtoken", read_env("NGROK_TOKEN")])

    subprocess.Popen(["./ngrok", "tcp", str(minecraft_port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Allow ngrok to initialize

    # Get the ngrok URL from the API
    url = "http://127.0.0.1:4040/api/tunnels"
    response = requests.get(url)
    data = json.loads(response.text)
    tcp_link = data['tunnels'][0]['public_url']
    print(tcp_link)
    return tcp_link
    
def download() -> None:
    from mega import Mega

    try:    
        mega = Mega()
        email, password = read_env("MEGA_EMAIL"), read_env("MEGA_PASSWORD")
        m = mega.login(email, password)
        
        try: 
            m.download(m.find("world.zip"))
            subprocess.run(["rm", "-rf", "world/"])
            print("wohohoho")

            os.system("unzip world.zip")

            print("Backup successfully unzipped")
            os.remove("world.zip")

        except Exception as e:
            print(f"NO BACKUP FOUND")
            print(e)

    except:
        print("Login failed")

def start_backup() -> None:
    from mega import Mega

    # Initialize and login to Mega
    try:    
        mega = Mega()
        email, password = read_env("MEGA_EMAIL"), read_env("MEGA_PASSWORD")
        m = mega.login(email, password)
        print("Login Successfull")

    except:
        print("Login failed")
        exit()

    while True:
        # Wait for the next interval
        time.sleep(upload_interval)

        send_command("save-off")
        send_command("save-all")

        zip_name = f'world_{int(time.time())}.zip'                  #
        os.system(f'zip -r {zip_name} {local_world_path}')          #zip

        m.upload(zip_name)                                          #upload the new zip file to Mega

        send_command("save-on")

        #delete old world
        old_file = m.find("world.zip")
        if old_file != None:
            m.destroy(old_file[0])

        m.rename(m.find(zip_name), "world.zip")                     #rename
        os.remove(zip_name)                                         #remove the local zip file after uploading

        print(f"Backup uploaded: {zip_name}")   


#main
while True:
    if isFirstRun():
        subprocess.run(["bash", "reset.sh"])

        #url from https://mcversions.net/download/1.21.1
        server_url = "https://piston-data.mojang.com/v1/objects/59353fb40c36d304f2035d51e7d6e6baa98dc05c/server.jar"
        urllib.request.urlretrieve(server_url, "server.jar")

        java_command = f"java -Xms{ram_amount}G -Xmx{ram_amount}G -jar server.jar nogui"

        # Launch the Minecraft server
        subprocess.run(java_command, shell=True)

        # Modify the eula.txt file to set 'true'
        with open("eula.txt", "w") as eula_file:
            eula_file.write("eula=true")

        server_properties = "server.properties"    
        # Read the file
        with open(server_properties, 'r') as file:
            lines = file.readlines()
        # Modify the specific line
        for i, line in enumerate(lines):
            if line.startswith("online-mode="):
                lines[i] = "online-mode=false\n"
                break
        # Write the modified content back to the file
        with open(server_properties, 'w') as file:
            file.writelines(lines)

        download()
        time.sleep(1)

    else:
        subprocess.run(["bash", "reset.sh"])
        main_thread = threading.Thread(target=start_server)
        ngrok_thread = threading.Timer(2, start_ngrok)
        backup_thread = threading.Timer(10, start_backup)
        input_thread = threading.Timer(12, manual_input)

        main_thread.start()
        ngrok_thread.start()
        backup_thread.start()
        input_thread.start()


        break
