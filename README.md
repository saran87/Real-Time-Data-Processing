# Real-Time-Data-Processing
Real Time Data Processing Server using Celery and Tornado for  http://pak-track.com/

### Install Requirements
```bash
pip install -r requirements.txt
```

### Start the Restful API
```bash
python start.py --port=8000 --db_host=test.pak-track.com --db=paktrackDB
```

### Start the celery workers
```bash
celery worker -A paktrack --loglevel=INFO -P processes --concurrency=3 -Q vibration -n worker2.%%h
celery worker -A paktrack --loglevel=INFO -P processes --concurrency=3 -Q shock -n worker2.%%h
celery worker -A paktrack --loglevel=INFO -P processes --concurrency=3 -Q vibration_report -n worker2.%%h
```

## Start the server using supervisor(Refer here for supervisor documentation http://supervisord.org/)

 1. Add `tornado.conf` & `celery.conf` to the supervisor config
 2. Start `supervisord`
 3. Check the process using `supervisorctl`
 4. You could also use https://flower.readthedocs.io/en/latest/ to monitor the celery workers
