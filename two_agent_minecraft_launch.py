import os
import signal
import psutil
import sys

from marlo.launch_minecraft_in_background import launch_minecraft_in_background
from pathlib import Path


def kill(processes):
    for process in processes:
        try:
            parent = psutil.Process(process.pid)
        except psutil.NoSuchProcess:
            return
        children = parent.children(recursive=True)
        for p in children:
            p.send_signal(signal.SIGTERM)

        os.kill(parent.pid, signal.SIGTERM)


minecraft_dir = Path("MalmoPlatform/Minecraft")

if not minecraft_dir.is_dir():
    print("Malmo Minecraft downloaded and build ...")
    try:
        import malmo
        from malmo.minecraftbootstrap import download
        download(branch="master", buildMod=True)
    except Exception as e:
        print("Could not download Marlo and build from GitHub: " + str(e))
        exit(1)

minecraft_path = str(minecraft_dir.absolute())
os.chdir(str(minecraft_dir))

print("Launching ...")
launch_processes = launch_minecraft_in_background(minecraft_path, [10000, 10001], replaceable=False)

if sys.platform == "darwin":
    # Minecraft launched in separate terminals.
    exit(0)

while True:
    quit = input("\nInput \"quit\" to stop launched Minecraft: ")
    if quit == "quit":
        break

print("Terminating Minecraft ...")

kill(launch_processes)
