import requests

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
except FileNotFoundError as e:
    print("keys file not found, try in another node")
