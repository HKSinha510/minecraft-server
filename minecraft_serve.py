import os
import subprocess

def isFirstRun():
    if os.path.isdir("./versions") & os.path.isdir("./libraries"):
        return False
    else:
        return True

if isFirstRun():
    subprocess.run(["bash", "minecraft.sh"])

else:
    subprocess.run(["java", "-Xms16G", "-Xmx16G", "-jar", "server.jar", "nogui"])

    with open("./.env") as e:
        print(f"./ngrok config add-authtoken {e.read().split('=')[1]}")

