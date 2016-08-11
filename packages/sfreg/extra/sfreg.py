#sfreg.py
import urllib.request
import requests
import json
import logging
import subprocess
import pickle
import os.path

#LOGGER
logging.basicConfig(level=logging.WARN, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger("sfreg")
logger.setLevel(logging.INFO)

def getIP():
    p = subprocess.Popen(['/opt/mesosphere/bin/detect_ip'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    IP, err = p.communicate()
    rc = p.returncode
    return IP.decode("utf-8").rstrip()


#CONSTANTS
URL_MESOS = "leader.mesos"
URL_MASTER = "http://" + URL_MESOS
URL_3DT = URL_MASTER + ":1050"
IP = getIP()
URL_CONSUL = "http://" + IP + ":8500"


#FUNCTIONS

def deregisterServiceInConsul( name ):
    url_deregister = URL_CONSUL + "/v1/agent/service/deregister/" + name
    return requests.get(url_deregister)

def registerServiceInConsul( name, address, checks ):
    #{
    #  "ID": "redis1",
    #  "Name": "redis",
    #  "Tags": [
    #    "master",
    #    "v1"
    #  ],
    #  "Address": "127.0.0.1",
    #  "Port": 8000,
    #  "Check": {
    #    "Script": "/usr/local/bin/check_redis.py",
    #    "HTTP": "http://localhost:5000/health",
    #    "Interval": "10s",
    #    "TTL": "15s"
    #  }
    #}
    url_register = URL_CONSUL + "/v1/agent/service/register"
    service = {}
    service["ID"] = name + ":" + address
    service["Name"] = name
    service["Address"] = address
    service["checks"] = checks
    requests.put(url_register, data=service)
    return requests.put(url_register, data=json.dumps(service))

def getServiceFabricComponents():
    logger.debug("getServiceFabricComponents from " + URL_MESOS)

    url_units = URL_3DT + "/system/health/v1/report"

    logger.debug("Getting units from " + url_units)
    #READ UNITS
    with urllib.request.urlopen(url_units) as response:
        data = json.loads(response.readall().decode('utf-8'))
    logger.debug(data)
    return data

def formatUnitName( name ):
    return name.rsplit('.',1)[0]

def getFilteredServiceFabricComponents():
    filtered = []
    toBeDiscarded = []

    serviceFabricComponents = getServiceFabricComponents()

    # check if discard and add to discard list
    for key, value in serviceFabricComponents["Units"].items():
        # discard timer services
        if value["UnitName"].endswith(".timer"):
            toBeDiscarded.append(value["UnitName"].replace(".timer",""))
            logger.debug("To be discarded: " + value["UnitName"])

    # filter
    for key, value in serviceFabricComponents["Units"].items():
            name = formatUnitName( value["UnitName"] )
            if name not in toBeDiscarded:
                item = value
                item["UnitName"] = name
                filtered.append(item)
                logger.debug("Adding " + name)
            else:
                logger.debug("Discarding " + name)

    return filtered



#MAIN
currentSF = []
filteredServiceFabricComponents = getFilteredServiceFabricComponents()

# Register current service fabric components
for value in filteredServiceFabricComponents:
    for node in value["Nodes"]:
        # filter by IP: own services
        if node["IP"] == IP:
          name = value["UnitName"]
          checks = [{'script':'systemctl status ' + name,'interval':'30s'}]
          r = registerServiceInConsul(name, IP, checks)
          logger.info("Registering " + name + " in " + IP + " -> " + str(r.status_code))
          currentSF.append(name)

# Unregister old ones
# read prev status file
prevSF = []
if os.path.isfile("sfstatus"):
  prevSF = pickle.load(open( "sfstatus", "rb" ))

# Deregister services present in previous synchronization and not now
for s in set(prevSF) - set(currentSF):
  r = deregisterServiceInConsul(s)
  logger.info("Deregistering " + s + " -> " + str(r.status_code))

# save status file for next execution
pickle.dump(currentSF,open( "sfstatus", "wb" ))

