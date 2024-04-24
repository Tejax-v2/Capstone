#**************************************************TEST CODE***********************************************

import subprocess
import csv

# Function to run ADB command and capture output
def run_adb_command(command):
    result = subprocess.run('adb '+command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# print(run_adb_command('shell getprop ro.product.model'))
# Function to write device information to CSV
def write_to_csv(device_info):
    with open('device_info.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Property', 'Value'])
        for key, value in device_info.items():
            writer.writerow([key, value])

print(run_adb_command('shell getprop'))
# Get device information using ADB commands
device_info = {
    'Device Model': run_adb_command('shell getprop ro.product.model'),
    'Android Version': run_adb_command('shell getprop ro.build.version.release'),
    'Build Number': run_adb_command('shell getprop ro.build.display.id'),
    'Verified Boot State': run_adb_command('shell getprop ro.boot.verifiedbootstate'),
    'VBMeta Device State': run_adb_command('shell getprop ro.boot.vbmeta.device_state'),
    'Crypto State': run_adb_command('shell getprop ro.crypto.state'),
    'GSM Roaming': run_adb_command('shell getprop gsm.operator.isroaming'),
    'GSM Alphalake': run_adb_command('shell getprop gsm.sim.operator.alpha'),
    'GSM SIM Alphalake': run_adb_command('shell getprop gsm.sim.operator.alpha'),
    'Debuggable': run_adb_command('shell getprop ro.debuggable'),
    'Secure': run_adb_command('shell getprop ro.secure'),
    'Build Tags': run_adb_command('shell getprop ro.build.tags'),
    'Init SVC': run_adb_command('shell getprop init.svc'),
    'Persist SYS': run_adb_command('shell getprop persist.sys'),
    'Hardware': run_adb_command('shell getprop ro.hardware'),
    'Security Patch': run_adb_command('shell getprop ro.build.version.security_patch'),
    # Add more properties as needed
}

# Write device information to CSV file
write_to_csv(device_info)

print("Device information has been dumped into device_info.csv")
