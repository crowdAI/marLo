import os
import signal
import psutil

from marlo.launch_minecraft_in_background import launch_minecraft_in_background


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


# Configure location of Minecraft TODO requires knowing exact install dir
if os.name == 'nt':
    minecraft_dir = "C:\malmo\MalmoPlatform\Minecraft"
else: 
    minecraft_dir = "~/MalmoPlatform/Minecraft"

os.chdir(minecraft_dir)

print("Launching ...")
launch_processes = launch_minecraft_in_background(minecraft_dir, [10000, 10001], replaceable=False)

# TODO Add agent code here.

print("Killing ...")

kill(launch_processes)
