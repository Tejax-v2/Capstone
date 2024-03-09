import subprocess
import os

def run_command(command):
    new_command = command.split()
    result = subprocess.run(new_command, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return result.stderr.strip()

def get_package_paths():
    # Execute adb shell pm list packages -f command
    output = subprocess.check_output(['adb', 'shell', 'pm', 'list', 'packages', '-f']).decode('utf-8')

    # Split the output by lines
    lines = output.strip().split('\n')
    # print(lines)
    # Extract file paths
    file_paths = [line.split('.apk=')[0].split(':', 1)[-1] for line in lines]

    return file_paths

# def main():
package_paths = get_package_paths()

    # Print the file paths
# pathlist = []
# for path in package_paths:
#     pathlist.append(path+".apk")
# print(pathlist)

# Create a directory to store the apks
if not os.path.exists('apks'):
    os.makedirs('apks')
for i in range(len(package_paths)):
    # print(package_paths[i])
    download = run_command(f"adb pull {package_paths[i]}.apk ./apks/{package_paths[i].split('/')[-1]}_{i}.apk")
    #renaming a file
    # os.rename(f'./apks/{package_paths[i]}.apk', f'./apks/{package_paths}_{i}.apk')


# if __name__ == "__main__":
    # main()
