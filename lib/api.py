from datetime import datetime
import json
import requests
import yaml

from .logger import Logger


class Api:


    def __init__(self):
        self.logger = Logger() 

    def getlocalisation(self, deviceId, deviceKey, dtStart):
        """ Récupération des localisations via l'API
        pour un capteur donné (device_id), de sa clés (deviceKey) 
        la date de dernière localisation (dtStart) n'est finalement 
        pas utile car le paramètre afterScts ou AfterAcquisition ne fonctionnent pas""" 
        
        #responses = requests.get('https://api.vectronic-wildlife.com/v3/collar/' + deviceId + '/gps?collarkey=' + deviceKey + '&afterScts=' + dtStart)
        responses = requests.get('https://api.vectronic-wildlife.com/v3/collar/' + deviceId + '/gps?collarkey=' + deviceKey)
        
        # https://api.vectronic-wildlife.com/collar/91888/gps?collarkey=77A64CA500D615D1848F3D5C732FD80661C44D708747143DD7CBD59E58382B4839EB793246B96C79E85A405EB0997183B7DC8F36EAA7BD2154AD173F928F69159A0875FBE52E1CBB623977240788BE079E1FF481AC25D79F69F474000BC925D774F8865C8B3CD59178C434587D138780D99C91CDC7EECF4BC0EF4F54204806083845F7902041ED4C245A758A216B45403936338EEDEEA7C2F6799ADB761EE782DCE0D9B6962E2361FE88158F8AE69E28733DCEA3AA7684DF5EF2E2CF253593327A57FF1F0DF330942401856333385097FB77D34E4F1138DFE16AA3CDD3CD2F368AAA60D7E3A3BEA06870CF5AE2BEBCF5E704D455755B859D5E230E48088362E5

        if responses.status_code != 200:
            self.logger.logWarning(
                code = "100",
                message = "Erreur lors de la récupération des données associées au capteur " + deviceId,
                exception = "" #responses.json()
            )
            return None
            
        return responses.json()
