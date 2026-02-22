from zoneinfo import ZoneInfo
from datetime import datetime

def get_time():
    uktime = datetime.now(ZoneInfo("Europe/London"))
    mvtime = datetime.now(ZoneInfo("Indian/Maldives"))
    
    return{
        "UK": uktime ,
        "MV": mvtime
    }

def get_date():
    date = datetime.now()
    date = date.strftime("%d %B %Y")
    return(date)

