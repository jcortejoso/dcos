import sys

from socket import inet_aton, error as socket_error
from subprocess import check_output, CalledProcessError


def write_str(filename, contents):
    with open(filename, 'w') as f:
        f.write(contents)


def invoke_detect_ip():
    try:
        ip = check_output(
            ['/opt/mesosphere/bin/detect_ip']).strip().decode('utf-8')
    except CalledProcessError as e:
        print("check_output exited with {}".format(e))
        sys.exit(1)
    try:
        inet_aton(ip)
        return ip
    except socket_error as e:
        print(
            "inet_aton exited with {}. {} is not a valid IPv4 address".format(e, ip))
        sys.exit(1)


detected_ip = invoke_detect_ip()

write_str("/opt/mesosphere/etc/vault.hcl",
          "listener"
          "\"tcp\" {address = \"0.0.0.0:8200\" tls_cert_file = \"/opt/mesosphere/etc/sds/secrets/gosec04.crt\" "
          "tls_key_file =\"/opt/mesosphere/etc/sds/secrets/gosec04.key\"}"
          "backend "
          "\"zookeeper\" {address = \"127.0.0.1:2181\" advertise_addr = \"https://" + detected_ip +
          ":8200\" path = \"vault\"}")
