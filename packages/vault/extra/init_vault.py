import subprocess

process = subprocess.Popen(["/opt/mesosphere/bin/vault", "init", "--ca-cert=/opt/mesosphere/etc/sds/secrets/ca-bundle.crt", "-tls-skip-verify"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

out, err = process.communicate()
rc = process.returncode

if rc != 1:
    with open('/opt/mesosphere/etc/sds/secrets/keys.txt', 'w') as f:
        f.write(out.decode('utf-8'))
else:
    print(err)
