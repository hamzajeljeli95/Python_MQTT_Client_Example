import paho.mqtt.client as mqtt
import logging
import time
import json
from SensorData import SensorData

# DEFINITION DES VARIABLES GLOABLES
broker_address = "41.229.118.249"
broker_port = 33820
username = "hamzajeljeli"
password = "21545049H@m"
clientid = "ESP8266-CLIENT1056"
sensorid = "SENSOR_LhDxlW248StPYdg"
mqtttopic = "/home/room/abdelkader"


# DEFINITION DES METHODES DE "CALLBACK"
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)
        client.bad_connection_flag = True


def on_disconnect(client, userdata, rc):
    logging.info("disconnecting reason  " + str(rc))
    client.connected_flag = False
    client.disconnect_flag = True


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_log(client, userdata, level, buf):
    print("log: ", buf)


# EXECUTION

# CREER UN NOUVEAU CLIENT MQTT
client = mqtt.Client(clientid)

# ATTRIBUTION DES METHODES DE CALLBACK
client.on_log = on_log
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# AFFECTER L'AUTHENTIFICATION AVEC USER\PASSWORD AU CLIENT MQTT
client.username_pw_set(username=username, password=password)

# CONNEXION AU BROKER ET ATTENTE D'ACQUITEMENT DE CONNEXION
client.connect(broker_address, port=broker_port)
time.sleep(5)

# DEMARRAGE DE PROCESS D'ECHANGE DE DONNEES AVEC LE SERVEUR
client.loop_start()

# CREATION D'UN NOUVEAU OBJET DE TYPE SENSORDATA AVEC LES INFORMATIONS NECESSAIRES
# GID = GatewayID
# SID = SensorID
# VAL = Valeur

value = 26  # VALEUR A ENVOYER
data = SensorData(gid=clientid, sid=sensorid, val=value)

# CONVERSION DE L'OBJET "data" VERS JSON ET PUBLICATION VERS BROKER
jsonfile = json.dumps(data, default=SensorData.convert_to_dict, indent=4, sort_keys=True)
print("Publishing message to topic", mqtttopic)
client.publish(mqtttopic, jsonfile)

# ATTENTE DE CALLBACK
time.sleep(10)

# ARRET ET DECONNEXION
client.loop_stop()
client.disconnect()
