from pytz import utc
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
}
job_defaults = {
    'coalesce': False,
    'max_instances': 10
}



#removes a minute in the time
def session_time(start_time,period):
    datetime_object = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    amin = datetime_object - datetime.timedelta(seconds=int(period))
    return amin

def post_time(start_time,period):
    datetime_object = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    amin = datetime_object + datetime.timedelta(seconds=int(period))
    return amin


SCHED = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)#, timezone=utc)

# schedi().start()