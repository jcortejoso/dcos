import subprocess
import requests
import json
import sys

check_unsealed_process = subprocess.Popen(["curl","--insecure","https://127.0.0.1:8200/v1/sys/health"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = check_unsealed_process.communicate()

try:
    json_response = json.loads(out.decode('utf-8'))

    if json_response['sealed'] == False:
        print("Vault already unsealed")
        sys.exit(0)

except Exception as e:
    print("Unable to check if vault is unsealed: "+str(e))

print("Vault not unsealed. Trying...")

try:
    with open('/opt/mesosphere/etc/stratio/secrets/keys.txt') as f:
        lines = f.readlines()
        masters = open('/opt/mesosphere/etc/master_list').read().strip()
        masters_ary = masters[1:-1].replace('"', "").replace(' ', "").split(',')
        for x in range(0, 3):
            line = lines[x]
            lineSplit = line.split()
            for master in masters_ary:
                rep = requests.put('https://' + master + ':8200/v1/sys/unseal', '{"key": "' + lineSplit[2] + '"}',
                               verify=False)
                # verify='/home/grubio/Descargas/ca-bundle.crt'
                print(str(rep.status_code) + " " + rep.text)
        print('vault unsealed successfully')
        sys.exit(0)
except FileNotFoundError as e:
    print("keys file not found, try in another node")
    sys.exit(1)
