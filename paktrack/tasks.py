from __future__ import absolute_import
from celery.utils.log import get_task_logger
from paktrack.celery import app

from paktrack.vibration import vibration
import logging.config
import logging

LOG_CONFIG = 'paktrack.logging.conf'

#logging.config.fileConfig(LOG_CONFIG)
logger = get_task_logger(__name__)


@app.task
def process_data(db_host, db_port, db, truck_id, package_id):
    vib = vibration.Vibration(db_host, db_port, db)
    return vib.process_data(truck_id,package_id)


@app.task
def hello_world(to='world'):
    return 'Hello {0}'.format(to)