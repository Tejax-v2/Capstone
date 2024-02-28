import subprocess
import csv
import os

file_name = "deviceinfo.csv"

file = open(file_name, "w")
writer = csv.writer(file)

def run_command(command):
    new_command = command.split()
    result = subprocess.run(new_command, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return result.stderr.strip()


getprop_out = run_command("adb shell getprop")
lines = getprop_out.splitlines()

properties = {}
for line in lines:
    parts = line.strip().split(':')
    if len(parts) == 2:
        key = parts[0].strip()[1:-1]  
        value = parts[1].strip()
        if value.startswith('[') and value.endswith(']'):  
            value = value[1:-1]  
        properties[key] = value

for key, value in properties.items():
    writer.writerow([key, value])

file.close()
print(properties.items())