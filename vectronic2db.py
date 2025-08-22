from lib.Database import Database
from lib.api import Api

# temporaire por test
from lib.logger import Logger
import json

def main():
    """Fonction principale de mise à jour des données GPS"""

    # Initialisation de la connexion à la base de données
    database = Database()

    # Création de l'objet API
    api = Api()

    # Récupération de la liste des capteur actif 
    # et de leur date de dernière synchronisation
    capteurs = database.selectCapteurs()

    # On boucle sur les capteurs pour récupérer les données
    for capteur in capteurs:
        capt_id = capteur['capt_id']
        deviceId = capteur['capt_id_constructeur']
        deviceKey = capteur['capt_key']
        dtStart = capteur['loc_date_utc'].strftime("%Y-%m-%dT%H:%M:%S")
        
        responses = api.getlocalisation(deviceId, deviceKey, dtStart)

        logger = Logger()

        if responses is not None:
            # On boucle sur les localisations GPS
            for response in responses:
                logger.writeLog("999-1", json.dumps(response))
                
                # On contrôle la date d'acuisition est postérieur à la dernière date renseignée en base 
                if (response['acquisitionTime'] > dtStart):

                    fix_statut_id = response['idFixType'] 
                    if (fix_statut_id != 0):
                        # On ajoute 10 pour faire référence au code 
                        # status corespondant aux colliers Vectronic 
                        # sauf si fix_statut_id = 0 car ça correspond 
                        # au No Fix (comme Lotek)
                        fix_statut_id = 10 
    
                    loc_dop = response['dop']
                    loc_temperature_capteur = response['temperature']
                    loc_date_capteur_utc = response['acquisitionTime']

                    if fix_statut_id != 0:

                        loc_long = response['longitude']
                        loc_lat = response['latitude']
                        loc_altitude_capteur = response['height']

                        database.insertLocData(
                            capt_id,
                            loc_long,
                            loc_lat,
                            loc_dop,
                            loc_altitude_capteur,
                            loc_temperature_capteur,
                            loc_date_capteur_utc,
                            None, #fix_status_id,
                            None #loc_nb_satellites
                        )

                    else :
                       loc_commentaire = 'Erreur : Pas de coordonnées'
                       loc_anomalie = True

                       database.insertNoLocData(
                           capt_id, 
                           loc_dop, 
                           loc_altitude_capteur, 
                           loc_temperature_capteur, 
                           loc_date_capteur_utc, 
                           loc_commentaire, 
                           loc_anomalie,
                           None, #fix_status_id,
                           None #loc_nb_satellites
                       )

                        
    database.close()

if __name__ == '__main__':
    main()



