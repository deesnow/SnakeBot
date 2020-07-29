import datetime
from botSettings import settings
import pandas

def singleton(cls, *args, **kw):
    """
    Singleton function
    """
    instances = {}
    def _singleton():
       if cls not in instances:
            instances[cls] = cls(*args, **kw)
       return instances[cls]
    return _singleton

@singleton
class jobsQueue(object):
    """
    jobsQueue is responsible to handle all shittybotAPI related API call, because of its rate limit.
    Generate ID for all new request, records it with date-time stamp.
    Rate Limit : 102 requests / 5 minute(s)
    
    """
    def __init__(self):
        self.headers = [ 'time','position', 'expired' ,'processed']
        self.df = pandas.DataFrame(columns=self.headers)
        self.settings = settings

    def add_request(self, uid):
        self.uid = uid
        self.now = datetime.datetime.now()
        self.update_expired()
        self.df.loc[self.uid] = [self.now, 0, False, False]
        self.get_qposition(self.uid)
        

    def get_qposition(self, uid):
        self.uid = uid
        self.df_q = self.df[self.df['processed']==False].sort_values(by=['time'])
        self.df_q['position'] = self.df_q['time'].rank()
        self.pos = int(self.df_q.loc[self.uid]['position'])
        self.settings.SHITTYBOT_REQUESTS = self.pos
        return self.pos


    def update_expired(self):
        self.df2 = self.df[self.df['time'] > datetime.datetime.now() - datetime.timedelta(minutes=5)]
        self.df = self.df2

    
    def last_position(self):
        pass


