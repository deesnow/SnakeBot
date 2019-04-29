import requests
import json
import logging

class Swgoh():
    def __init__(self,):
        self.base_url = "https://swgoh.gg/api/player/"
        self.logger = logging.getLogger(__name__)
        self.payload = ""
        self.header = {
            'User-Agent': "SnakeBot/0.0.1",
            'Accept': "*/*",
            'Connection': "keep-alive"
        }
    
    def swgoh_getuser(self, allycode):
        self.allycode = allycode
        self.url = self.base_url + str(self.allycode)


        try:
            self.response = requests.request("GET", self.url, data=self.payload)
            self.logger.info('Response 200 OK')

            return json.loads(self.response.text)
            
        except Exception as error:
            self.logger.exception('GET url is failed - [{}]'.format(error))

            return None

    




        
