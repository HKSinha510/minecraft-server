import os
import time
from mega import Mega
import zipfile

def zip_directory(directory_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory_path))

def read_env(environment_variable) -> str:
    with open("./.env") as f:
        lines = {j.split("=")[0]: j.split("=")[1] for j in [i.strip() for i in f.readlines()]}
        return lines[environment_variable]
    
def download():
    try:    
        mega = Mega()
        email, password = read_env("MEGA_EMAIL"), read_env("MEGA_PASSWORD")
        m = mega.login(email, password)
        print("Login Successfull")

    except:
        print("Login failed")
        exit()

    m.download(m.find("world.zip"))

    # Run the unzip command using os.system()
    exit_status = os.system("unzip world.zip -d ./world")

    # Check if the command was successful
    if exit_status == 0:
        print("Backup successfully unzipped")
        os.remove("world.zip")
    else:
        print(f"Unzipping failed with exit status: {exit_status}")
        exit()
    

def backup_main():
    # Initialize and login to Mega
    try:    
        mega = Mega()
        email, password = read_env("MEGA_EMAIL"), read_env("MEGA_PASSWORD")
        m = mega.login(email, password)
        print("Login Successfull")

    except:
        print("Login failed")
        exit()

    local_world_path = './world/'       #path
    upload_interval = 700               #interval

    while True:
        # Wait for the next interval
        time.sleep(upload_interval)

        zip_name = f'world_{int(time.time())}.zip'
        os.system(f'zip -r {zip_name} {local_world_path}')  # comment this if on windows system
        #zip_directory('world/', zip_name)                  # use this if on windows system

        # Upload the new zip file to Mega
        uploaded_file = m.upload(zip_name)

        #delete old world
        old_file = m.find("world.zip")
        if old_file != None:
            m.destroy(old_file[0])

        #rename
        m.rename(m.find(zip_name), "world.zip")

        # Remove the local zip file after uploading
        os.remove(zip_name)
        print(f"Backup uploaded: {zip_name}")

if __name__ == "__main__":
    backup_main( )