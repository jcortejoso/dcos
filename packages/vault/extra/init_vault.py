import subprocess
import json
import sys

check_initialized_process = subprocess.Popen(["curl","--insecure","https://127.0.0.1:8200/v1/sys/health"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = check_initialized_process.communicate()


try:
    json_response = json.loads(out.decode('utf-8'))

    if json_response['initialized'] == True:
        print("Vault already initialized")
        sys.exit(0)

except Exception as e:
    print("Unable to check if vault is intialized: "+str(e))

print("Vault not initialized. Initializing...")

process = subprocess.Popen(["/opt/mesosphere/bin/vault", "init", "--ca-cert=/opt/mesosphere/etc/stratio/secrets/ca-bundle.crt", "-tls-skip-verify"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

out, err = process.communicate()
rc = process.returncode

if rc != 1:
    with open('/opt/mesosphere/etc/stratio/secrets/keys.txt', 'w') as f:
        f.write(out.decode('utf-8'))
        sys.exit(0)
else:
    print(err)
    sys.exit(1)
