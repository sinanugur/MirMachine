from ..models import Job
from engine.scripts.mirmachine_args import run_mirmachine
from .socket_helper import announce_status_change, announce_queue_position, announce_initiation, announce_completed
from .maintainer import clean_up_temporary_files
from django.utils import timezone
from MirMachineWebapp import user_config as config


def schedule_job(stop):
    ongoing = Job.objects.filter(status='ongoing')
    # check if already job running
    if ongoing.exists():
        return
    queued = Job.objects.filter(status='queued').order_by('initiated')
    # check if queue is empty
    if not queued.exists():
        if config.AUTO_CLEANUP_TEMP_FILES:
            clean_up_temporary_files()
        return
    next_in_line = queued[0]
    next_in_line.status = 'ongoing'
    next_in_line.initiated = timezone.now()
    next_in_line.save()
    announce_status_change(next_in_line)
    announce_initiation(next_in_line)
    for i in range(len(queued)):
        announce_queue_position(queued[i], i+1)
    try:
        process, job_object = run_mirmachine(next_in_line, stop)
        handle_job_end(process, job_object)
    except OSError:
        next_in_line.status = 'halted'
        next_in_line.save()
        announce_status_change(next_in_line)
    except RuntimeError:
        print('Interrupted, exiting thread')
        return
    except AttributeError:
        next_in_line.status = 'halted'
        next_in_line.save()
        announce_status_change(next_in_line) # TODO add extra parameter letting them know to try different input
    schedule_job(stop)


def handle_job_end(process, job_object):
    if process.returncode != 0:
        job_object.status = 'halted'
    else:
        job_object.status = 'completed'
    job_object.completed = timezone.now()
    job_object.save()
    announce_completed(job_object)
    announce_status_change(job_object)





