from flask import Flask, render_template, request
from utilities import run_command
from pdfmaker import make_pdf

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def mail_handler():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        try:
            mail = request.form['mail']
            ip_addr = request.remote_addr
            print(f"[INFO] - Request from {ip_addr}")
            print(f"[INFO] - Email to {mail}")
            print(f"[INFO] - Trying to connect via ADB...")
            conn_command = f"adb connect {ip_addr}:5555"
            result = run_command(conn_command)
            print(f"[INFO] - ADB Output: {result}")
        except:
            return render_template('index.html',status='danger',info="Missing argument 'mail'")
        return render_template('index.html',status='success',info=f"Success: {ip_addr}")
    
@app.route('/usb', methods=['GET','POST'])
def usb_handler():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        try:
            mail = request.form['mail']
        except:
            return render_template('index.html',status='danger',info="Missing argument 'mail'!")
        ip_addr = request.remote_addr
        print(f"[INFO] - Request from {ip_addr}")
        print(f"[INFO] - Email to {mail}")
        print(f"[INFO] - Trying to connect via ADB...")
        conn_command = f"adb connect {ip_addr}:5555"
        result = run_command(conn_command)
        if len(result.splitlines()) < 2:
            return render_template('index.html',status='danger',info=f"Device connection Failed!")
        print(f"[INFO] - ADB Output: {result}")
        result = run_command("adb shell getprop")
        result = result.splitlines()
        output = {}
        for line in result:
            linepair = line.split(":")
            if len(linepair) < 2:
                continue
            processed_list = [item.strip().strip('[]') for item in linepair]
            output[f"{processed_list[0]}"] = processed_list[1]
        # print(output)
        specs = {}
        specs['Device Manufacturer'] = output['ro.product.manufacturer'] if 'ro.product.manufacturer' in output else '-' 
        specs['Device Model'] = output['ro.product.model'] if 'ro.product.model' in output else '-'
        specs['Android Version'] = output['ro.build.version.release'] if 'ro.build.version.release' in output else '-'
        specs['SDK Version'] = output['ro.build.version.sdk'] if 'ro.build.version.sdk' in output else '-'
        specs['Host OS'] = output['ro.build.host'] if 'ro.build.host' in output else '-'
        specs['Security Patch'] = output['ro.build.version.security_patch'] if 'ro.build.version.security_patch' in output else '-'
        specs['Display ID'] = output['ro.build.display.id'] if 'ro.build.display.id' in output else '-'
        specs['Device Family'] = output['ro.build.device_family'] if 'ro.build.device_family' in output else '-'
        specs['Minimum supported SDK'] = output['ro.build.version.min_supported_target_sdk'] if 'ro.build.version.min_supported_target_sdk' in output else '-'
        specs['Default User'] = output['ro.build.user'] if 'ro.build.user' in output else '-'
        specs['Rooted'] = output['ro.build.system_root_image'] if 'ro.build.system_root_image' in output else '-'
        specs['Dalvik Image Format'] = output['dalvik.vm.appimageformat'] if 'dalvik.vm.appimageformat' in output else '-'
        specs['Block Size'] = output['dalvik.vm.dex2oat-max-image-block-size'] if 'dalvik.vm.dex2oat-max-image-block-size' in output else '-'

        battery = run_command('adb shell dumpsys battery')
        batterystats = {}
        for line in battery.splitlines()[1:]:
            linepair = line.split(":")
            batterystats[f"{linepair[0].strip()}"] = linepair[1].strip() if len(linepair) == 2 else '-'
        battery_info = {}

        status_codes = ['Discharging','Charging','Not Charging','Full']
        health_codes = ['Unknown','Good','Overheat','Dead','Overvoltage','Unspecified Failure']

        battery_info['AC powered'] = batterystats['AC powered'] if 'AC powered' in batterystats else '-'
        battery_info['USB powered'] = batterystats['USB powered'] if 'USB powered' in batterystats else '-'
        battery_info['Wireless powered'] = batterystats['Wireless powered'] if 'Wireless powered' in batterystats else '-'
        battery_info['Maximum Current'] = batterystats['Max charging current'] if 'Max charging current' in batterystats else '-'
        battery_info['Maximum Voltage'] = batterystats['Max charging voltage'] if 'Max charging voltage' in batterystats else '-'
        print(batterystats['Charge counter'],type(batterystats['Charge counter']))
        battery_info['Accumulated Charge'] = f"{int(batterystats['Charge counter'])/1000} mAh" if 'Charge counter' in batterystats else '-'
        battery_info['Charging Status'] = f"{status_codes[int(batterystats['status'])-1]}" if 'status' in batterystats else '-'
        battery_info['Battery Health'] = f"{health_codes[int(batterystats['health'])-1]}" if 'health' in batterystats else '-'
        battery_info['Battery Present'] = batterystats['present'] if 'present' in batterystats else '-'
        battery_info['Battery Level'] = f"{batterystats['level']}%" if 'level' in batterystats else '-'
        battery_info['Max Level'] = f"{batterystats['scale']}%" if 'scale' in batterystats else '-'
        battery_info['Current Voltage'] = f"{batterystats['voltage']} mV" if 'voltage' in batterystats else '-'
        battery_info['Temperature'] = f"{int(batterystats['temperature'])/10} C" if 'temperature' in batterystats else '-'
        battery_info['Technology'] = batterystats['technology'] if 'technology' in batterystats else '-'


        memory = run_command('adb shell cat /proc/meminfo')
        memory = memory.splitlines()
        memory_info = {}
        for idx,line in enumerate(memory):
            memtuple = line.split(':')
            memory_info[f"{memtuple[0].strip()}"] = memtuple[1].strip()
            if idx > 25:
                break

        make_pdf(specs,battery_info, memory_info)
        
        return render_template('index.html',status='success',info=f"Success: {ip_addr}")
        
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
