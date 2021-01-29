import os
print('Установка пакетов')
os.system('sudo apt update')
os.system('sudo apt upgrade')
os.system('sudo apt-get install net-tools')
os.system('mkdir /usr/share/outlinevpn')
print('Установка скрипта')
with open('/usr/share/outlinevpn/app.py', 'w') as f:
    f.write('''#!/usr/bin/python3
from flask import Flask, request, jsonify
import os
app = Flask(__name__)
@app.route('/', methods=['POST'])
def data():
    port = request.json['port']
    s  = os.popen("netstat -ant | grep :"+str(port)+" | grep ESTABLISHED | awk >
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
print('Добавление срипта в автозагрузку')
with open('/etc/systemd/system/outlinevpn.service', 'w') as f:
    f.write('''[Unit]
After=network.target
[Service]
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
LimitNOFILE=51200
ExecStart=/root/app.py
[Install]
WantedBy=default.target''')
print('Запуск')
os.system('systemctl start outlinevpn')
os.system('systemctl enable outlinevpn')
print('Успешно')