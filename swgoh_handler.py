import requests
import json
import logging

class Swgoh():
    def __init__(self,):
        self.base_url = "https://swgoh.gg/api/"
        self.logger = logging.getLogger(__name__)
        self.payload = ""
        self.header = {
            'User-Agent': "SnakeBot/1.2",
            'Accept': "*/*",
            'Connection': "keep-alive"
        }
    
    def swgoh_getuser(self, allycode):
        self.allycode = allycode
        self.url = self.base_url + 'player/' + str(self.allycode)


        try:
            self.response = requests.request("GET", self.url, data=self.payload)
            self.logger.info('Response 200 OK')

            if self.response != None:
                return json.loads(self.response.text)

            else:
                return None
                self.logger.error(f'Response for {self.allycode} was empty!')
            
        except Exception as error:
            self.logger.exception('GET url is failed - [{}]'.format(error))

            return None

    def swgoh_getmods(self, allycode):
        self.allycode = allycode
        self.url = self.base_url + 'players/' + str(self.allycode) + '/mods'


        try:
            self.response = requests.request("GET", self.url, data=self.payload)
            self.logger.info('Response 200 OK')

            return json.loads(self.response.text)
            
        except Exception as error:
            self.logger.exception('GET url is failed - [{}]'.format(error))

            return None
    




        
