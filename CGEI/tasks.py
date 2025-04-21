from celery import shared_task
from celery import Celery
from celery.schedules import crontab
import time
app = Celery()



@shared_task
def testDanierl3():
    print('ADD PRODUCT')