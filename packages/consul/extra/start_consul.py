#!/opt/mesosphere/bin/python
import os
import sys
import socket
from socket import inet_aton, error as socket_error
from subprocess import check_call, check_output, CalledProcessError


def get_var_assert_set(name):
    if name not in os.environ:
        print('ERROR: "{}" must be set'.format(name))
        sys.exit(1)

    return os.environ[name]


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

# Base for building up the command line
consul_cmdline = [
    'consul',
    'agent',
    '-bind', detected_ip,
    '-data-dir', '/var/lib/dcos/consul',
]

# Make necessary consul runtime directories
check_call(['mkdir', '-p', '/var/lib/dcos/consul'])

# Older systemd doesn't support RuntimeDirectory, make one if systemd didn't.
check_call(['mkdir', '-p', '/run/consul'])

masters = open('/opt/mesosphere/etc/master_list').read().strip()
masters_ary = masters[1:-1].replace('"', "").strip().split(',')

iam_server = False

if detected_ip in masters_ary:
    iam_server = True
    print("Node in Master list. Starting Consul as server")
    print("Starting UI in this node")
    consul_cmdline += [
        '-server',
        '-ui',
        '-ui-dir', '$PKG_PATH/ui',
    ]
else:
    print("Node not in Master list. Starting Consul as agent")

# TODO(jcortejoso): Check if this can cause a race condition (two servers bootstraping at the same time)
# Check for other Consul Servers already running
found_server = False

print(masters_ary)

for master in masters_ary:
    if not found_server:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((master, 8302))
        if result == 0:
            print("{server} has Consul running. Joining to its quorum".format(
                server=master))
            consul_cmdline += [
                "-join", master,
            ]
            found_server = True
        else:
            print("Not Consul listening in", master)

if not found_server and iam_server:
    print("Consul Server up not found. Starting this node with bootstrap")
    consul_cmdline += [
        "-bootstrap"
    ]
else:
    # We are running a Consul agent but no servers is up.
    # Anyway we join to all possible servers
    for master in masters_ary:
        consul_cmdline += [
            "-join", master,
        ]


# Start Consul
print("Running consul as command:", consul_cmdline)
sys.stdout.flush()
os.execv('/opt/mesosphere/bin/consul', consul_cmdline)
