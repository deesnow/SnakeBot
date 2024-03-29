"""
Created on Tue Sep  4  2018

@author: martrepodi

aiohttp modification made by: deesnow

Built upon code borrowed from platzman and shittybill
"""

#import requests
import aiohttp
#import asyncio
from json import loads, dumps
import time
from botSettings import settings as mysettings
import logging

class async_swgoh_help():
    def __init__(self, settings):
        self.logger = logging.getLogger(__name__)
        self.user = "username=" + settings.username
        self.user += "&password=" + settings.password
        self.user += "&grant_type=password"
        self.user += "&client_id=" + settings.client_id
        self.user += "&client_secret=" + settings.client_secret

        self.token = {}
        self.logged_in = False

        self.urlBase = 'https://api.swgoh.help'
        self.signin = '/auth/signin'
        self.endpoints = {'guilds': '/swgoh/guilds',
                          'players': '/swgoh/players',
                          'roster': '/swgoh/roster',
                          'data': '/swgoh/data',
                          'units': '/swgoh/units',
                          'zetas': '/swgoh/zetas',
                          'squads': '/swgoh/squads',
                          'events': '/swgoh/events',
                          'battles': '/swgoh/battles'}

        if settings.charStatsApi:
            self.charStatsApi = settings.charStatsApi
        else:
            self.charStatsApi = 'https://crinolo-swgoh.glitch.me/testCalc/api'

        self.verbose = settings.verbose if settings.verbose else False
        self.debug = settings.debug if settings.debug else False
        self.dump = settings.dump if settings.dump else False

        self.data_type = {'guild':'/swgoh/guild/',
                          'player':'/swgoh/player/',
                          'data':'/swgoh/data/',
                          'units':'/swgoh/units',
                          'battles':'/swgoh/battles'}

        #Extend Roster with crinilo_stats
        self.crinolo = CrinoloStat()
        self.logger = logging.getLogger(__name__)
    
    async def _getAccessToken(self):
        # if 'expires' in self.token.keys():
        #     token_expire_time = self.token['expires']
        #     if token_expire_time > time.time():
        #         return(self.token)
        signin_url = self.urlBase+self.signin
        payload = self.user
        head = {"Content-type": "application/x-www-form-urlencoded"}

        async with aiohttp.ClientSession() as session:
            async with session.post(signin_url, headers=head, data=payload, timeout=20) as self.r:
                if self.r.status != 200:
                    error = "Login failed!"
                    self.logger.error(f'{error} - Status:{self.r.status} - API Server is DOWN!')
                    return  {"status_code" : self.r.status,
                            "message": error}
                    
                    
                response = await self.r.json()

                self.token = { 'Authorization': "Bearer " + response['access_token'],
                            'expires': time.time() + response['expires_in'] - 300}
                return self.token
        



   

    async def fetchAPI(self, url, payload):
        await self._getAccessToken()
        if self.token == {}:
            return {'Error': 'API HIBA, az API nem elérhető'}
        head = {'Content-Type': 'application/json', 'Authorization': self.token['Authorization']}
        data_url = self.urlBase + url
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(data_url, headers=head, data=dumps(payload)) as self.r:
                    if self.r.status != 200:
                        error = "Login failed!"
                        self.data =  {"status_code" : self.r.status,
                                "message": error}
                    else:
                        self.data = await self.r.json()
        except Exception as e:
            self.data = {"message": 'Cannot fetch data'}
        
        return self.data
        




    def fetchPlayers(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['players'], payload)
            
        except Exception as e:
            return {'Error' : 'Fetch player data Failed, possinle API Error'}
            self.logger.error('Fetch player data Failed, possinle API Error')

    def fetchGuilds(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['guilds'], payload)
        except Exception as e:
            return str(e)

    # def fetchUnits(self, payload):
    #     if type(payload) == list:
    #         p = {}
    #         p['allycodes'] = payload
    #         p['enums'] = True
    #         payload = p
    #     elif type(payload) == int:
    #         p = {}
    #         p['allycodes'] = [payload]
    #         p['language'] = "eng_us"
    #         p['enums'] = True
    #         payload = p
    #     elif type(payload) != dict:
    #         return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
    #     try:
    #         return self.fetchAPI(self.endpoints['units'], payload)
    #     except Exception as e:
    #         return str(e)

    def fetchRoster(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['roster'], payload)
            
            
        except Exception as e:
            return str(e)

class settings():
    def __init__(self, _username, _password, **kwargs):
        self.username = _username
        self.password = _password
        self.client_id = kwargs.get('client_id', '123')
        self.client_secret = kwargs.get('client_secret', 'abc')
        self.charStatsApi = kwargs.get('charStatsApi', '')
        self.verbose = kwargs.get('verbose', False)
        self.debug = kwargs.get('debug', False)
        self.dump = kwargs.get('dump', False)


#### CrinoloStat #############################################################

class CrinoloStat():
    """
    *** NOT READY YET ***
    
    When the CrinoloStats modul will be available this part will extend the sittyBotApi
    and add calculated statistical data to the player raw player roster data.
    
    
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_crinolo_url = 'http://' + mysettings.CRINOLO_IP + ':' + mysettings.CRINOLO_PORT + '/api/' 




    async def fetch_sdata(self, payload):

        self.crin_payload = dumps(payload)
        head = {'Content-Type': 'application/json'}

        

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_crinolo_url, headers=head, data=self.crin_payload) as self.r:
                    if self.r.status != 200:
                        error = "Get Stats Failed"
                        self.data =  {"status_code" : self.r.status,
                                "message": error}
                        
                    else:
                        self.data = await self.r.json()
        except Exception as e:
            self.data = {"message": 'Cannot fetch Stats data from Crinolo'}
        
        return  self.data

