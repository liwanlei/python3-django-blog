import time
from datetime import  datetime as  dates
import datetime
def time_plus(endtime,starttime):
    endtime=dates.strftime(endtime,"%H:%M:%S")
    starttime=dates.strftime(starttime,"%H:%M:%S")
    time_a = dates.strptime(starttime,'%H:%M:%S')
    time_b = dates.strptime(endtime,'%H:%M:%S')
    td= (time_b-time_a).seconds
    return td
if __name__=='__main__':
    endtime=dates.now()
    #time.sleep(5)
    starttime=dates.now()
    print(time_plus(endtime,starttime))
