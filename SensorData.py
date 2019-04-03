class SensorData:

    def __init__(self, gid, sid, val):
        self.GID = gid
        self.SID = sid
        self.VAL = val

# convert_to_dict PERMET DE CONVERTIR L'OBJET SENSORDATA VERS UN DICTIONNAIRE POUR FACILITER SON CONVERSION
# VERS UN OBJET JSON.

    def convert_to_dict(obj):

        obj_dict = {
        }

        obj_dict.update(obj.__dict__)

        return obj_dict
