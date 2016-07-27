from __future__ import absolute_import

from celery import Celery

app = Celery('paktrack')

app.config_from_object('paktrack.celeryconfig')

if __name__ == '__main__':
    app.start()

