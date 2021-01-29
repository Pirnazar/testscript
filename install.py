import os
print('Установка пакетов')
os.system('sudo apt update')
os.system('sudo apt upgrade -y')
os.system('sudo apt-get install net-tools')
os.system('pip3 install flask')
os.system('mkdir /usr/share/outlinevpn')
print('Installing script...')
with open('/usr/share/outlinevpn/app.py', 'w') as f:
    f.write('''#!/usr/bin/python3
from flask import Flask, request, jsonify
import os
app = Flask(__name__)
@app.route('/', methods=['POST'])
def data():
    port = request.json['port']
    s  = os.popen("netstat -ant | grep :"+str(port)+" | grep ESTABLISHED | awk '{print $5}'").read().split()
    ips = []
    for i in s:
        i = i.split(':')
        for a in i:
            if len(a)>6:
                ips.append(a)
    ips = list(set(ips))
    return jsonify({'ips':ips})

if __name__ == '__main__':
    app.run(host='0.0.0.0')''')
os.system('chmod 777 /usr/share/outlinevpn/app.py')
print('Adding to autostart')
with open('/etc/systemd/system/outlinevpn.service', 'w') as f:
    f.write('''[Unit]
After=network.target
[Service]
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
LimitNOFILE=51200
ExecStart=/usr/share/outlinevpn/app.py
[Install]
WantedBy=default.target''')
print('Start')
os.system('systemctl start outlinevpn')
os.system('systemctl enable outlinevpn')
print('Success')