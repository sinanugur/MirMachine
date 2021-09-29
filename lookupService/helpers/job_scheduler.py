import threading
from ..models import Job
from engine.scripts.mirmachine_args import run_mirmachine


def schedule_job():
    ongoing = Job.objects.filter(status='ongoing')
    if ongoing.exists():
        return
    queued = Job.objects.filter(status='queued').order_by('initiated')
    # could check if none are returned, but this should never happen
    next_in_line = queued[0]
    next_in_line.status = 'ongoing'
    next_in_line.save()
    run_mirmachine(next_in_line)

def handle_job_complete():
    pass
