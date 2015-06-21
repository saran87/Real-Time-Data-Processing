; ===================================================
;  PakTrack celery vibration report worker supervisor
; ====================================================

[program:celery_consolidated_report]
; Set full path to celery program if using virtualenv
command=celery worker -A paktrack --loglevel=INFO -P processes -Q vibration_report -n worker1.%%h
directory=/home/vagrant/Code/celery_tornado/
stdout_logfile=/var/log/celery/vib_report_worker.log
stderr_logfile=/var/log/celery/vib_report_worker_err.log
autostart=true
autorestart=true
startsecs=10
user=root
; Need to wait for currently executing tasks to finish at shutdown.
; Increase this if you have very long running tasks.
stopwaitsecs = 600

; When resorting to send SIGKILL to the program to terminate it
; send SIGKILL to its whole process group instead,
; taking care of its children as well.
killasgroup=true

; if rabbitmq is supervised, set its priority higher
; so it starts first
priority=998

; ==============================================
;  PakTrack celery vibration worker supervisor
; ==============================================
[program:celery_vibration]
; Set full path to celery program if using virtualenv
command=celery worker -A paktrack --loglevel=INFO -P processes -Q vibration -n worker2.%%h
directory=/home/vagrant/Code/celery_tornado/
stdout_logfile=/var/log/celery/vibration_worker.log
stderr_logfile=/var/log/celery/vibration_worker_err.log
autostart=true
autorestart=true
startsecs=10
user=root
; Need to wait for currently executing tasks to finish at shutdown.
; Increase this if you have very long running tasks.
stopwaitsecs = 600

; When resorting to send SIGKILL to the program to terminate it
; send SIGKILL to its whole process group instead,
; taking care of its children as well.
killasgroup=true

; if rabbitmq is supervised, set its priority higher
; so it starts first
priority=997

; ===========================================
;  PakTrack celery shock worker supervisor
; ===========================================

[program:celery_shock]
; Set full path to celery program if using virtualenv
command=celery worker -A paktrack --loglevel=INFO -P processes -Q shock -n worker3.%%h
directory=/home/vagrant/Code/celery_tornado/
stdout_logfile=/var/log/celery/shock_worker.log
stderr_logfile=/var/log/celery/shock_worker_err.log
autostart=true
autorestart=true
startsecs=10
user=root
; Need to wait for currently executing tasks to finish at shutdown.
; Increase this if you have very long running tasks.
stopwaitsecs = 600

; When resorting to send SIGKILL to the program to terminate it
; send SIGKILL to its whole process group instead,
; taking care of its children as well.
killasgroup=true

; if rabbitmq is supervised, set its priority higher
; so it starts first
priority=996