#****************************************************TEST CODE*********************************************

import subprocess

# Check if adb is installed
try:
    subprocess.run(["adb", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    print("ADB is not installed. Please install Android Debug Bridge (ADB) to use this script.")
    exit(1)

# Get list of installed packages
packages_process = subprocess.run(["adb", "shell", "pm", "list", "packages", "-f"], capture_output=True, text=True)
packages = packages_process.stdout.splitlines()
base_applist = [element for element in packages if element.startswith("package:/data")]
print(len(packages))
print(len(base_applist))

def write_to_csv(device_info):
    with open('device_info.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Property', 'Value'])
        for key, value in device_info.items():
            writer.writerow([key, value])

csvfile = open('version_info.csv', 'w')

# Iterate through each package
for package in base_applist:
    new_pack = package.split("base.apk=")
    new_pack[0] = new_pack[0].replace("package:", "")
    print(new_pack[1], end="   ")

    # Get version name
    version_process = subprocess.run(["adb", "shell", "dumpsys", "package", new_pack[1]], capture_output=True, text=True)
    version_info = version_process.stdout.splitlines()
    version_name = next((line.split("=")[1] for line in version_info if "versionName" in line), None)
    print(version_name)
    csvfile.write(new_pack[1] + "," + version_name + "\n")