from __future__ import absolute_import
from celery.utils.log import get_task_logger
from paktrack.celery import app

from paktrack.vibration import (vibration,consolidated_report,vibration_data_processor)
from paktrack.shock import (shock,shock_data_processor)
import logging.config
import logging

LOG_CONFIG = 'paktrack.logging.conf'

#logging.config.fileConfig(LOG_CONFIG)
logger = get_task_logger(__name__)


@app.task
def consolidated_report(db_host, db_port, db, db_user, db_pass, truck_id, package_id):
    vib = vibration.Vibration(db_host, db_port, db, db_user, db_pass)
    report = consolidated_report.ConsolidatedReport(vib)
    return report.process_data(truck_id,package_id)
 
@app.task
def process_vibration(db_host, db_port, db, db_user, db_pass, id):
    vib = vibration.Vibration(db_host, db_port, db, db_user, db_pass)
    data_processor = vibration_data_processor.VibrationDataProcessor(vib)
    return data_processor.pre_process_data(id)

@app.task
def process_shock(db_host, db_port, db, db_user, db_pass, id):
    shock_model = shock.Shock(db_host, db_port, db, db_user, db_pass)
    data_processor = shock_data_processor.ShockDataProcessor(shock_model)
    return data_processor.pre_process_data(id)